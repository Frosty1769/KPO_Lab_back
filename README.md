# Кассовое приложение - Backend

## Описание
Backend для кассового приложения на Flask с SQLite и SQLAlchemy.

## Стек технологий
- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-RESTX
- Flask-CORS
- SQLite

## Структура проекта
```
KPO_Lab_back/
├── app.py                 # Точка входа приложения
├── db.py                  # Инициализация SQLAlchemy
├── init_db.py             # Скрипт инициализации БД
├── API_DOCS.md            # Документация API
├── model/
│   └── model.py           # Модели БД (User, Product)
├── db_actions/
│   ├── user.py            # Логика работы с пользователями
│   └── products.py        # Логика работы с товарами
├── endpoints/
│   ├── user.py            # Эндпоинты для пользователей
│   └── products.py        # Эндпоинты для товаров
└── scr/
    └── core.py            # Конфигурация приложения
```

## Установка зависимостей

```powershell
pip install flask flask-sqlalchemy flask-restx flask-cors
```

## Инициализация базы данных

```powershell
python init_db.py
```

Это создаст:
- Таблицы `users` и `products`
- Администратора по умолчанию (логин: `admin`, пароль: `admin`)

## Запуск сервера

```powershell
python app.py
```

Сервер запустится на `http://localhost:5000`

## API Endpoints

### Пользователи
- `POST /api/user/login` - Вход в систему
- `POST /api/user/register` - Регистрация пользователя
- `GET /api/user/info` - Информация о текущем пользователе
- `POST /api/user/logout` - Выход
- `GET /api/user/list` - Список всех пользователей (только админ)

### Товары
- `POST /api/products/add` - Добавить товар (только админ)
- `GET /api/products/list` - Получить список товаров
- `GET /api/products/article/<article>` - Получить товар по артикулу
- `DELETE /api/products/delete/<article>` - Удалить товар (только админ)
- `POST /api/products/sale` - Обработка продажи

Подробнее см. [API_DOCS.md](API_DOCS.md)

## Транзакции

Все операции изменения данных используют уровень изоляции `SERIALIZABLE` для обеспечения консистентности при конкурентном доступе.

## Тестирование

Для unit-тестирования используйте pytest:

```powershell
pip install pytest
pytest test.py
```

## Готовность к упаковке в EXE

Приложение спроектировано для возможности упаковки в `.exe` с помощью PyInstaller:

```powershell
pip install pyinstaller
pyinstaller --onefile --add-data "instance;instance" app.py
```
