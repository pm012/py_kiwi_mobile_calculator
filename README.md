# kiwi_mobile
Python mobile application (calculator) using Kiwi

project_root/
│
├── src/
│   ├── __init__.py
│   ├── engine.py          # Модель калькулятора та безпечний обчислювач
│   ├── strategies.py      # Стратегії математичних операцій
│   └── ui.py              # Kivy UI (View)
│
├── tests/
│   ├── __init__.py
│   ├── test_engine.py     # Тести бізнес-логіки
│   └── test_strategies.py # Тести операторів та edge cases
│
├── main.py                # Точка входу в додаток
├── requirements.txt
└── pytest.ini


Install poetry and run: 

poetry install 
