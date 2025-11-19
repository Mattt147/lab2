# Lab2

Описание проекта

## Структура проекта

```
lab2/
├── main.py                 # Точка входа
├── package/
│   ├── __init__.py
│   ├── models.py          # Модуль 1: классы данных
│   ├── calculations.py    # Модуль 2: бизнес-логика
│   └── exporters.py       # Модуль 3: экспорт в doc/xls
├── README.md
├── requirements.txt
└── tests/
```

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## Тестирование

```bash
python -m pytest tests/
```

