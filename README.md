# Dolphin AntiDetect

Минимальный прототип AntiDetect браузера для Dolphin эмулятора.

## Структура

```
Dolphin-AntiDetect/
├── README.md
├── .gitignore
└── src/
    ├── main.py          # Основной движок
    ├── profiler.py      # Профилирование браузера
    └── detector.py      # Детектор антивектора
```

## Быстрый старт

```bash
cd Dolphin-AntiDetect
pip install -r requirements.txt
python src/main.py
```

## Основные возможности

- Профилирование пользовательского агента
- Фingerprint браузеров
- Базовая защита от детекции

## Лицензия

MIT
