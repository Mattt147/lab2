"""
Модуль models.py
Содержит классы для представления отделочных материалов
"""


class Material:
    """Базовый класс для отделочного материала"""
    
    def __init__(self, name, price_per_unit, unit_coverage):
        """
        Инициализация материала
        
        Args:
            name (str): Название материала
            price_per_unit (float): Цена за единицу (рулон/упаковку/м²)
            unit_coverage (float): Покрытие одной единицы в м²
        """
        self.name = name
        self.price_per_unit = price_per_unit
        self.unit_coverage = unit_coverage
    
    def __str__(self):
        return f"{self.name} - {self.price_per_unit}₽ за единицу (покрытие: {self.unit_coverage}м²)"
    
    def __repr__(self):
        return f"Material('{self.name}', {self.price_per_unit}, {self.unit_coverage})"


class Wallpaper(Material):
    """Класс для обоев"""
    
    def __init__(self, name, price_per_roll, roll_width=0.53, roll_length=10.05):
        """
        Инициализация обоев
        
        Args:
            name (str): Название обоев
            price_per_roll (float): Цена за рулон
            roll_width (float): Ширина рулона в метрах (стандарт 0.53м)
            roll_length (float): Длина рулона в метрах (стандарт 10.05м)
        """
        coverage = roll_width * roll_length
        super().__init__(name, price_per_roll, coverage)
        self.roll_width = roll_width
        self.roll_length = roll_length
    
    def __str__(self):
        return f"Обои '{self.name}' - {self.price_per_unit}₽/рулон ({self.roll_width}×{self.roll_length}м)"
    
    def __repr__(self):
        return f"Wallpaper('{self.name}', {self.price_per_unit}, {self.roll_width}, {self.roll_length})"


class Tile(Material):
    """Класс для плитки"""
    
    def __init__(self, name, price_per_box, tiles_per_box, tile_width=0.3, tile_height=0.3):
        """
        Инициализация плитки
        
        Args:
            name (str): Название плитки
            price_per_box (float): Цена за упаковку
            tiles_per_box (int): Количество плиток в упаковке
            tile_width (float): Ширина плитки в метрах
            tile_height (float): Высота плитки в метрах
        """
        tile_area = tile_width * tile_height
        coverage = tile_area * tiles_per_box
        super().__init__(name, price_per_box, coverage)
        self.tiles_per_box = tiles_per_box
        self.tile_width = tile_width
        self.tile_height = tile_height
    
    def __str__(self):
        return f"Плитка '{self.name}' - {self.price_per_unit}₽/упаковка ({self.tiles_per_box}шт, {self.tile_width}×{self.tile_height}м)"
    
    def __repr__(self):
        return f"Tile('{self.name}', {self.price_per_unit}, {self.tiles_per_box}, {self.tile_width}, {self.tile_height})"


class Laminate(Material):
    """Класс для ламината"""
    
    def __init__(self, name, price_per_pack, planks_per_pack, plank_width=0.193, plank_length=1.380):
        """
        Инициализация ламината
        
        Args:
            name (str): Название ламината
            price_per_pack (float): Цена за упаковку
            planks_per_pack (int): Количество досок в упаковке
            plank_width (float): Ширина доски в метрах
            plank_length (float): Длина доски в метрах
        """
        plank_area = plank_width * plank_length
        coverage = plank_area * planks_per_pack
        super().__init__(name, price_per_pack, coverage)
        self.planks_per_pack = planks_per_pack
        self.plank_width = plank_width
        self.plank_length = plank_length
    
    def __str__(self):
        return f"Ламинат '{self.name}' - {self.price_per_unit}₽/упаковка ({self.planks_per_pack}шт, {self.plank_width}×{self.plank_length}м)"
    
    def __repr__(self):
        return f"Laminate('{self.name}', {self.price_per_unit}, {self.planks_per_pack}, {self.plank_width}, {self.plank_length})"


class CalculationResult:
    """Класс для хранения результатов расчёта"""
    
    def __init__(self, material, area, units_needed, total_cost, reserve_percent=10):
        """
        Инициализация результата расчёта
        
        Args:
            material (Material): Материал
            area (float): Площадь для покрытия (м²)
            units_needed (int): Необходимое количество единиц
            total_cost (float): Общая стоимость
            reserve_percent (float): Процент запаса
        """
        self.material = material
        self.area = area
        self.units_needed = units_needed
        self.total_cost = total_cost
        self.reserve_percent = reserve_percent
    
    def __str__(self):
        return (f"Результат расчёта:\n"
                f"Материал: {self.material.name}\n"
                f"Площадь: {self.area}м²\n"
                f"Необходимо единиц: {self.units_needed}\n"
                f"Общая стоимость: {self.total_cost:.2f}₽\n"
                f"Запас: {self.reserve_percent}%")
    
    def __repr__(self):
        return f"CalculationResult({self.material.name}, {self.area}, {self.units_needed}, {self.total_cost})"