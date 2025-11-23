# Unit Tests для KPO_Lab_back

Этот каталог содержит модульные тесты для проверки корректности работы backend-приложения кассовой системы.

## Структура тестов

- `test_models.py` - Тесты моделей данных (User, Product, SoldProduct)
- `test_user.py` - Тесты управления пользователями (регистрация, вход, удаление)
- `test_products.py` - Тесты управления товарами и обработки продаж

## Установка зависимостей

Перед запуском тестов необходимо установить pytest:

```bash
pip install pytest
```

## Запуск тестов

### Запуск всех тестов:
```bash
python -m pytest unit_tests/ -v
```

### Запуск конкретного файла с тестами:
```bash
python -m pytest unit_tests/test_models.py -v
python -m pytest unit_tests/test_user.py -v
python -m pytest unit_tests/test_products.py -v
```

### Запуск конкретного тестового класса:
```bash
python -m pytest unit_tests/test_products.py::TestSalesProcessing -v
```

### Запуск конкретного теста:
```bash
python -m pytest unit_tests/test_products.py::TestSalesProcessing::test_process_sale_success -v
```

### Запуск с выводом покрытия кода (опционально):
```bash
pip install pytest-cov
python -m pytest unit_tests/ --cov=db_actions --cov=model --cov-report=html
```

## Описание тестовых наборов

### test_models.py
Проверяет корректность работы методов моделей данных:
- `to_dict()` - сериализация в словарь
- `__repr__()` - строковое представление
- Проверка всех полей моделей

### test_user.py
Проверяет функции управления пользователями:
- Регистрация новых пользователей
- Вход в систему с проверкой пароля
- Получение информации о пользователе
- Удаление пользователей (с защитой от самоудаления)
- Получение списка всех пользователей

### test_products.py
Проверяет функции управления товарами и продажами:
- Добавление/удаление товаров
- Поиск товаров по артикулу
- Обработка продаж с автоматическим списанием
- Проверка недостаточного количества товара
- Генерация агрегированного отчёта о продажах
- Очистка истории продаж
- Изоляция транзакций (SERIALIZABLE)

## Особенности реализации

### Тестовая база данных
Тесты используют SQLite в памяти (`sqlite:///:memory:`), которая создаётся заново для каждого тестового модуля. Это обеспечивает изоляцию тестов и быстрое выполнение.

### Фикстуры
- `app` - создаёт тестовое Flask-приложение с инициализированной БД
- `client` - создаёт тестовый клиент для работы с сессиями

### Проверка транзакций
Тест `test_transaction_isolation` проверяет корректность работы уровня изоляции `SERIALIZABLE` при последовательных продажах одного товара.

## Ожидаемый результат

При успешном прохождении всех тестов вы должны увидеть:

```
============================= test session starts =============================
collected 25 items

unit_tests/test_models.py::TestUserModel::test_user_to_dict PASSED       [  4%]
unit_tests/test_models.py::TestUserModel::test_user_repr PASSED          [  8%]
unit_tests/test_models.py::TestProductModel::test_product_to_dict PASSED [ 12%]
...
============================= 25 passed in 0.45s ==============================
```

## Troubleshooting

### ModuleNotFoundError: No module named 'pytest'
Установите pytest: `pip install pytest`

### ImportError при запуске тестов
Убедитесь, что вы запускаете тесты из корневой директории проекта (где находится `app.py`), используя `python -m pytest unit_tests/`

### Ошибки связанные с сессией Flask
Некоторые тесты требуют контекст Flask-приложения. Убедитесь, что используется фикстура `app` и тесты выполняются внутри `with app.app_context():`
