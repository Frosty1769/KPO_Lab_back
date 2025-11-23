# API Документация - Кассовое приложение

## Базовый URL
```
http://localhost:5000/api
```

## Аутентификация
Все запросы используют сессионную аутентификацию через cookies. После логина сессия сохраняется автоматически.

---

## Пользователи (User API)

### POST /api/user/login
**Описание:** Аутентификация пользователя  
**Доступ:** Все

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (Success):**
```json
{
  "status": "ok",
  "data": {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "isAdmin": true
  }
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Неправильный логин"
}
```

---

### POST /api/user/register
**Описание:** Регистрация нового пользователя (кассира или админа)  
**Доступ:** Все (но рекомендуется вызывать только от имени админа)

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "role": "cashier"  // "cashier" или "admin"
}
```

**Response (Success):**
```json
{
  "status": "ok",
  "message": "Пользователь создан"
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Имя пользователя занято"
}
```

---

### GET /api/user/info
**Описание:** Получение информации о текущем авторизованном пользователе  
**Доступ:** Авторизованные пользователи

**Response (Success):**
```json
{
  "status": "ok",
  "data": {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "isAdmin": true
  }
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Не авторизован"
}
```

---

### POST /api/user/logout
**Описание:** Выход из системы  
**Доступ:** Авторизованные пользователи

**Response:**
```json
{
  "status": "ok",
  "message": "Вышли из системы"
}
```

---

### GET /api/user/list
**Описание:** Получение списка всех пользователей  
**Доступ:** Только администратор

**Response (Success):**
```json
{
  "status": "ok",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "role": "admin",
      "created_at": "2025-11-23T12:00:00"
    },
    {
      "id": 2,
      "username": "cashier1",
      "role": "cashier",
      "created_at": "2025-11-23T13:00:00"
    }
  ]
}
```

---

## Товары (Products API)

### POST /api/products/add
**Описание:** Добавление товара на склад или увеличение количества существующего  
**Доступ:** Только администратор

**Request Body:**
```json
{
  "article": "ART001",
  "name": "Молоко 3.2%",
  "price": 89.90,
  "quantity": 50
}
```

**Response (Success - новый товар):**
```json
{
  "status": "ok",
  "message": "Товар добавлен",
  "data": {
    "id": 1,
    "article": "ART001",
    "name": "Молоко 3.2%",
    "price": 89.90,
    "quantity": 50,
    "created_at": "2025-11-23T12:00:00",
    "updated_at": "2025-11-23T12:00:00"
  }
}
```

**Response (Success - обновление количества):**
```json
{
  "status": "ok",
  "message": "Количество товара обновлено",
  "data": {
    "id": 1,
    "article": "ART001",
    "name": "Молоко 3.2%",
    "price": 89.90,
    "quantity": 100,
    "created_at": "2025-11-23T12:00:00",
    "updated_at": "2025-11-23T13:00:00"
  }
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Доступ запрещён"
}
```

---

### GET /api/products/list
**Описание:** Получение списка всех товаров на складе  
**Доступ:** Все авторизованные пользователи

**Response (Success):**
```json
{
  "status": "ok",
  "data": [
    {
      "id": 1,
      "article": "ART001",
      "name": "Молоко 3.2%",
      "price": 89.90,
      "quantity": 50,
      "created_at": "2025-11-23T12:00:00",
      "updated_at": "2025-11-23T12:00:00"
    },
    {
      "id": 2,
      "article": "ART002",
      "name": "Хлеб белый",
      "price": 45.50,
      "quantity": 30,
      "created_at": "2025-11-23T12:00:00",
      "updated_at": "2025-11-23T12:00:00"
    }
  ]
}
```

---

### GET /api/products/article/<article>
**Описание:** Получение товара по артикулу  
**Доступ:** Все авторизованные пользователи

**URL Parameters:**
- `article` - артикул товара (например, ART001)

**Response (Success):**
```json
{
  "status": "ok",
  "data": {
    "id": 1,
    "article": "ART001",
    "name": "Молоко 3.2%",
    "price": 89.90,
    "quantity": 50,
    "created_at": "2025-11-23T12:00:00",
    "updated_at": "2025-11-23T12:00:00"
  }
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Товар не найден"
}
```

---

### DELETE /api/products/delete/<article>
**Описание:** Удаление товара из базы  
**Доступ:** Только администратор

**URL Parameters:**
- `article` - артикул товара (например, ART001)

**Response (Success):**
```json
{
  "status": "ok",
  "message": "Товар удалён"
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Доступ запрещён"
}
```

---

### POST /api/products/sale
**Описание:** Обработка продажи (списание товаров со склада)  
**Доступ:** Все авторизованные пользователи (кассиры и админы)

**Request Body:**
```json
{
  "items": [
    {
      "article": "ART001",
      "quantity": 2
    },
    {
      "article": "ART002",
      "quantity": 1
    }
  ]
}
```

**Response (Success):**
```json
{
  "status": "ok",
  "message": "Продажа завершена",
  "data": {
    "items": [
      {
        "article": "ART001",
        "name": "Молоко 3.2%",
        "price": 89.90,
        "quantity": 2,
        "total": 179.80
      },
      {
        "article": "ART002",
        "name": "Хлеб белый",
        "price": 45.50,
        "quantity": 1,
        "total": 45.50
      }
    ],
    "total_price": 225.30
  }
}
```

**Response (Error - недостаточно товара):**
```json
{
  "status": "error",
  "message": "Недостаточно товара Молоко 3.2% на складе. Доступно: 1"
}
```

**Response (Error - товар не найден):**
```json
{
  "status": "error",
  "message": "Товар ART001 не найден"
}
```

---

## Коды статусов HTTP

- `200 OK` - Успешный запрос
- `400 Bad Request` - Некорректные данные запроса
- `401 Unauthorized` - Не авторизован
- `403 Forbidden` - Доступ запрещён (недостаточно прав)
- `404 Not Found` - Ресурс не найден
- `500 Internal Server Error` - Ошибка сервера

---

## Примечания по работе с транзакциями

Все операции изменения данных (добавление товаров, продажа) используют уровень изоляции `SERIALIZABLE` для предотвращения конфликтов при одновременном доступе нескольких пользователей.

При продаже товаров используется блокировка строк (`with_for_update()`), чтобы избежать race conditions при списании товаров.

---

## Пример использования (curl)

### Логин
```bash
curl -X POST http://localhost:5000/api/user/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' \
  -c cookies.txt
```

### Добавление товара
```bash
curl -X POST http://localhost:5000/api/products/add \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"article": "ART001", "name": "Молоко", "price": 89.90, "quantity": 50}'
```

### Получение списка товаров
```bash
curl -X GET http://localhost:5000/api/products/list \
  -b cookies.txt
```

### Продажа товаров
```bash
curl -X POST http://localhost:5000/api/products/sale \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"items": [{"article": "ART001", "quantity": 2}]}'
```
