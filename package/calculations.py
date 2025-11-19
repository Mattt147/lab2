"""
Модуль calculations.py
Содержит логику расчёта количества и стоимости отделочных материалов
"""

import math
from .models import Material, CalculationResult


class MaterialCalculator:
    """Класс для расчёта количества и стоимости материалов"""
    
    def __init__(self, reserve_percent=10):
        """
        Инициализация калькулятора
        
        Args:
            reserve_percent (float): Процент запаса материала (по умолчанию 10%)
        """
        self._reserve_percent = reserve_percent
        self._calculations_history = []
    
    @property
    def reserve_percent(self):
        """Получить процент запаса"""
        return self._reserve_percent
    
    @reserve_percent.setter
    def reserve_percent(self, value):
        """
        Установить процент запаса
        
        Args:
            value (float): Новый процент запаса
        
        Raises:
            ValueError: Если процент отрицательный или больше 100
        """
        if value < 0 or value > 100:
            raise ValueError("Процент запаса должен быть от 0 до 100")
        self._reserve_percent = value
    
    def calculate(self, material, area):
        """
        Рассчитать количество материала и стоимость
        
        Args:
            material (Material): Объект материала
            area (float): Площадь для покрытия в м²
        
        Returns:
            CalculationResult: Результат расчёта
        
        Raises:
            ValueError: Если площадь отрицательная или материал некорректен
        """
        if area <= 0:
            raise ValueError("Площадь должна быть положительным числом")
        
        if not isinstance(material, Material):
            raise ValueError("Параметр material должен быть экземпляром класса Material")
        
        # Учитываем запас
        area_with_reserve = area * (1 + self._reserve_percent / 100)
        
        # Рассчитываем количество единиц (округляем вверх)
        units_needed = math.ceil(area_with_reserve / material.unit_coverage)
        
        # Рассчитываем общую стоимость
        total_cost = units_needed * material.price_per_unit
        
        # Создаём результат
        result = CalculationResult(
            material=material,
            area=area,
            units_needed=units_needed,
            total_cost=total_cost,
            reserve_percent=self._reserve_percent
        )
        
        # Сохраняем в историю
        self._calculations_history.append(result)
        
        return result
    
    def get_history(self):
        """
        Получить историю всех расчётов
        
        Returns:
            list: Список объектов CalculationResult
        """
        return self._calculations_history.copy()
    
    def clear_history(self):
        """Очистить историю расчётов"""
        self._calculations_history.clear()
    
    def compare_materials(self, materials, area):
        """
        Сравнить несколько материалов для одной площади
        
        Args:
            materials (list): Список объектов Material
            area (float): Площадь для покрытия
        
        Returns:
            list: Список результатов расчётов, отсортированных по стоимости
        """
        if not materials:
            raise ValueError("Список материалов не может быть пустым")
        
        results = []
        for material in materials:
            result = self.calculate(material, area)
            results.append(result)
        
        # Сортируем по стоимости (от меньшей к большей)
        results.sort(key=lambda r: r.total_cost)
        
        return results
    
    def __str__(self):
        return f"MaterialCalculator(запас: {self._reserve_percent}%, расчётов выполнено: {len(self._calculations_history)})"
    
    def __repr__(self):
        return f"MaterialCalculator(reserve_percent={self._reserve_percent})"


class RoomCalculator:
    """Класс для расчёта материалов для комнат со сложной геометрией"""
    
    def __init__(self):
        """Инициализация калькулятора комнат"""
        self._material_calculator = MaterialCalculator()
    
    @property
    def reserve_percent(self):
        """Получить процент запаса"""
        return self._material_calculator.reserve_percent
    
    @reserve_percent.setter
    def reserve_percent(self, value):
        """Установить процент запаса"""
        self._material_calculator.reserve_percent = value
    
    def calculate_floor_area(self, length, width):
        """
        Рассчитать площадь пола
        
        Args:
            length (float): Длина комнаты в метрах
            width (float): Ширина комнаты в метрах
        
        Returns:
            float: Площадь в м²
        """
        if length <= 0 or width <= 0:
            raise ValueError("Длина и ширина должны быть положительными")
        return length * width
    
    def calculate_wall_area(self, perimeter, height, door_area=0, window_area=0):
        """
        Рассчитать площадь стен с вычетом дверей и окон
        
        Args:
            perimeter (float): Периметр комнаты в метрах
            height (float): Высота потолка в метрах
            door_area (float): Площадь дверей в м²
            window_area (float): Площадь окон в м²
        
        Returns:
            float: Площадь стен в м²
        """
        if perimeter <= 0 or height <= 0:
            raise ValueError("Периметр и высота должны быть положительными")
        if door_area < 0 or window_area < 0:
            raise ValueError("Площади дверей и окон не могут быть отрицательными")
        
        total_wall_area = perimeter * height
        result_area = total_wall_area - door_area - window_area
        
        if result_area <= 0:
            raise ValueError("Площадь стен после вычета дверей и окон должна быть положительной")
        
        return result_area
    
    def calculate_materials_for_room(self, material, length, width, height=None, 
                                     door_area=0, window_area=0, surface_type='floor'):
        """
        Рассчитать материалы для комнаты
        
        Args:
            material (Material): Материал
            length (float): Длина комнаты
            width (float): Ширина комнаты
            height (float): Высота потолка (для стен)
            door_area (float): Площадь дверей
            window_area (float): Площадь окон
            surface_type (str): Тип поверхности ('floor' или 'wall')
        
        Returns:
            CalculationResult: Результат расчёта
        """
        if surface_type == 'floor':
            area = self.calculate_floor_area(length, width)
        elif surface_type == 'wall':
            if height is None:
                raise ValueError("Для расчёта стен необходимо указать высоту")
            perimeter = 2 * (length + width)
            area = self.calculate_wall_area(perimeter, height, door_area, window_area)
        else:
            raise ValueError("surface_type должен быть 'floor' или 'wall'")
        
        return self._material_calculator.calculate(material, area)
    
    def __str__(self):
        return f"RoomCalculator(запас: {self.reserve_percent}%)"
    
    def __repr__(self):
        return f"RoomCalculator()"


def validate_positive_number(value, name="Значение"):
    """
    Валидация положительного числа
    
    Args:
        value: Проверяемое значение
        name (str): Название параметра для сообщения об ошибке
    
    Returns:
        float: Валидированное значение
    
    Raises:
        ValueError: Если значение не является положительным числом
    """
    try:
        num = float(value)
        if num <= 0:
            raise ValueError(f"{name} должно быть положительным числом")
        return num
    except (TypeError, ValueError):
        raise ValueError(f"{name} должно быть числом")