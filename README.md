# Netflix Cash Flow Analysis

Проект по анализу денежных потоков компании Netflix с использованием API Alpha Vantage, библиотек Pandas и Matplotlib.

## Описание

Данный проект представляет собой комплексный анализ финансовой отчетности Netflix, включающий:
- Получение данных о денежных потоках через Alpha Vantage API
- Обработку и структурирование финансовых данных
- Расчет ключевых финансовых показателей
- Визуализацию динамики денежных потоков
- Анализ трендов с использованием скользящих средних

## Возможности

- **Загрузка данных**: Автоматическое получение годовых отчетов о денежных потоках
- **Анализ показателей**:
  - Операционный денежный поток (Operating Cash Flow)
  - Капитальные затраты (Capital Expenditures)
  - Дивидендные выплаты (Dividend Payout)
  - Свободный денежный поток (Free Cash Flow)
- **Визуализация**: Построение графиков динамики показателей
- **Статистический анализ**: Расчет скользящих средних (2 и 3 года)

## Структура проекта

netflix-cashflow-analysis/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── .gitignore
├── src/
│ ├── init.py
│ ├── data_loader.py
│ ├── data_processor.py
│ └── visualizer.py
├── notebooks/
│ └── analysis.ipynb
├── data/
│ └── .gitkeep
└── output/
└── .gitkeep

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/netflix-cashflow-analysis.git
cd netflix-cashflow-analysis

Установите зависимости:

pip install -r requirements.txt

Получите API ключ:
Зарегистрируйтесь на Alpha Vantage
Получите бесплатный API ключ
