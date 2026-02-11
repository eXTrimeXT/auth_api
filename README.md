# Система аутентификации и авторизации
Собственная система аутентификации и авторизации, реализованная на FastAPI с использованием гибкой системы ролей и прав доступа.

## Описание системы
Это полностью кастомная система аутентификации и авторизации, не использующая встроенные возможности фреймворка "из коробки".

### Ключевые особенности:
- **Регистрация и аутентификация пользователей** с хэшированием паролей
- **Гибкая система ролей** (admin, manager, user, guest)
- **Гранулярные права доступа** к бизнес-объектам
- **Разделение прав**: доступ к своим объектам / доступ ко всем объектам
- **JWT-токены** для безопасной аутентификации
- **Soft delete** пользователей (аккаунты не удаляются физически)
- **Административный интерфейс** для управления ролями и правилами доступа
- **Mock бизнес-объекты** для демонстрации работы системы

## Схема базы данных

### Основные таблицы:

#### 1. `users` - Пользователи системы
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор |
| `email` | String | Email (уникальный) |
| `hashed_password` | String | Хэшированный пароль |
| `first_name` | String | Имя |
| `last_name` | String | Фамилия |
| `middle_name` | String | Отчество (опционально) |
| `is_active` | Boolean | Активен ли пользователь |
| `created_at` | DateTime | Дата создания |
| `role_id` | Integer | Внешний ключ на роль |

#### 2. `roles` - Роли пользователей
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор |
| `name` | String | Название роли (уникальное) |
| `description` | Text | Описание роли |

**Стандартные роли:**
- `admin` - Полный доступ ко всему
- `manager` - Управление бизнес-объектами
- `user` - Базовый доступ
- `guest` - Ограниченный доступ (только чтение)

#### 3. `business_elements` - Бизнес-объекты
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор |
| `name` | String | Название объекта (уникальное) |
| `description` | Text | Описание |

**Примеры бизнес-объектов:**
- `users` - Управление пользователями
- `products` - Каталог товаров
- `orders` - Заказы
- `stores` - Магазины
- `access_rules` - Правила доступа

#### 4. `access_role_rules` - Правила доступа
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный идентификатор |
| `role_id` | Integer | Внешний ключ на роль |
| `business_element_id` | Integer | Внешний ключ на бизнес-объект |
| `read_permission` | Boolean | Чтение своих объектов |
| `read_all_permission` | Boolean | Чтение всех объектов |
| `create_permission` | Boolean | Создание объектов |
| `update_permission` | Boolean | Обновление своих объектов |
| `update_all_permission` | Boolean | Обновление всех объектов |
| `delete_permission` | Boolean | Удаление своих объектов |
| `delete_all_permission` | Boolean | Удаление всех объектов |

### Логика прав доступа:

- **`*_permission`** (без `all`) - действия только с объектами, созданными самим пользователем
- **`*_all_permission`** - действия со всеми объектами в системе

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/eXTrimeXT/auth_api
cd auth_api
```

### 2. Создание виртуального окружения

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных PostgreSQL

Создайте базу данных:

```sql
CREATE DATABASE auth_db;
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql://postgres:password@localhost/auth_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Важно:** Замените `password` на ваш пароль от PostgreSQL.

## Быстрый запуск

### 1. Инициализация базы данных

```bash
python init_db.py
```

После успешной инициализации вы увидите:

```
База данных успешно инициализирована!
Админ: admin@example.com / admin123
```

### 2. Запуск сервера

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Или используйте встроенный скрипт:

```bash
python main.py
```

### 3. Доступ к документации

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## API Endpoints

### Аутентификация

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| `POST` | `/auth/register` | Регистрация пользователя | Все |
| `POST` | `/auth/login` | Вход в систему | Все |
| `POST` | `/auth/logout` | Выход из системы | Авторизованные |

### Пользователи

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| `GET` | `/users/me` | Получить информацию о себе | Авторизованные |
| `PUT` | `/users/me` | Обновить профиль | Авторизованные |
| `DELETE` | `/users/me` | Удалить аккаунт (soft delete) | Авторизованные |

### Администрирование

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| `POST` | `/admin/roles` | Создать роль | Администратор |
| `GET` | `/admin/roles` | Получить все роли | Администратор |
| `POST` | `/admin/business-elements` | Создать бизнес-элемент | Администратор |
| `POST` | `/admin/access-rules` | Создать правило доступа | Администратор |
| `GET` | `/admin/access-rules` | Получить все правила доступа | Администратор |

### Mock бизнес-объекты

| Метод | Endpoint | Описание | Доступ |
|-------|----------|----------|--------|
| `GET` | `/mock/products` | Получить список продуктов | С правом чтения |
| `POST` | `/mock/products` | Создать продукт | С правом создания |
| `PUT` | `/mock/products/{id}` | Обновить продукт | С правом обновления |
| `DELETE` | `/mock/products/{id}` | Удалить продукт | С правом удаления |
| `GET` | `/mock/orders` | Получить список заказов | С правом чтения |
| `POST` | `/mock/orders` | Создать заказ | С правом создания |

## Примеры использования

### 1. Регистрация нового пользователя

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "middle_name": "Smith"
  }'
```

**Ответ:**
```json
{
  "id": 2,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "middle_name": "Smith",
  "is_active": true,
  "role_id": 3,
  "created_at": "2026-02-11T10:30:00"
}
```

### 2. Вход в систему

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Получение информации о текущем пользователе

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Ответ:**
```json
{
  "id": 1,
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "middle_name": null,
  "is_active": true,
  "role_id": 1,
  "created_at": "2026-02-11T10:00:00"
}
```

### 4. Создание продукта (требует прав)

```bash
curl -X POST "http://localhost:8000/mock/products" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Product 1",
    "owner_id": 1
  }'
```

### 5. Получение списка ролей (требует прав администратора)

```bash
curl -X GET "http://localhost:8000/admin/roles" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "admin",
    "description": "Administrator with full access"
  },
  {
    "id": 2,
    "name": "manager",
    "description": "Manager with business access"
  },
  {
    "id": 3,
    "name": "user",
    "description": "Regular user"
  },
  {
    "id": 4,
    "name": "guest",
    "description": "Guest with limited access"
  }
]
```

### 6. Создание правила доступа (администратор)

```bash
curl -X POST "http://localhost:8000/admin/access-rules" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 3,
    "business_element_id": 2,
    "read_permission": true,
    "read_all_permission": true,
    "create_permission": true,
    "update_permission": true,
    "update_all_permission": false,
    "delete_permission": true,
    "delete_all_permission": false
  }'
```

## Примеры прав доступа
### Роль: `admin` (Полный доступ)

| Бизнес-объект | Чтение | Чтение всех | Создание | Обновление | Обновление всех | Удаление | Удаление всех |
|---------------|--------|-------------|----------|------------|-----------------|----------|---------------|
| `users` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `products` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `orders` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `stores` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `access_rules` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Роль: `manager` (Управление бизнесом)

| Бизнес-объект | Чтение | Чтение всех | Создание | Обновление | Обновление всех | Удаление | Удаление всех |
|---------------|--------|-------------|----------|------------|-----------------|----------|---------------|
| `users` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `products` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `orders` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `stores` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `access_rules` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Роль: `user` (Базовый доступ)

| Бизнес-объект | Чтение | Чтение всех | Создание | Обновление | Обновление всех | Удаление | Удаление всех |
|---------------|--------|-------------|----------|------------|-----------------|----------|---------------|
| `users` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `products` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| `orders` | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `stores` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `access_rules` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Роль: `guest` (Только чтение)

| Бизнес-объект | Чтение | Чтение всех | Создание | Обновление | Обновление всех | Удаление | Удаление всех |
|---------------|--------|-------------|----------|------------|-----------------|----------|---------------|
| `users` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `products` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `orders` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `stores` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `access_rules` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

