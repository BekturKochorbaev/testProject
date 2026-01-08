# Django + Stripe Checkout (Pet Project)

Тестовый pet-проект на **Django**, демонстрирующий базовую e-commerce логику:

- товары и скидки  
- формирование заказов  
- оплата через **Stripe Checkout**  
- работа с заказами через админку  

Проект предназначен для **локальной разработки и обучения**.

---

##  Стек технологий

- Python 3.10+
- Django
- Stripe API
- SQLite (локально)
- PostgeSQL(в проде)
- Docker
- AWS(EC2)
- SSL Let's Encrypt

---

##  Установка и запуск проекта

### 1️ Клонировать репозиторий

```bash
git clone <repository_url>
cd <project_directory>
```

### 2 Создать и активировать виртуальное окружение

```bash
python -m venv venv
``` 

### Windows
```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

### 3 Установить зависимости

```bash
pip install -r requirements.txt
```

# Настройка проекта
### База данных (локальная разработка)

### Проект использует SQLite для локальной разработки.

### В settings.py:
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```
#  Миграции

## Примените миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание суперпользователя
```bash
python manage.py createsuperuser
```
## Приложение будет доступно по адресу:
```commandline
https://api.alimmah.dev
```
## Админ-панель
### Админка Django:
```commandline
https://api.alimmah.dev/admin/
```
### Через админку можно:

- создавать товары (Item)

- создавать скидки (Discount)

- добавлять товары в заказы (Order)

- управлять заказами и их статусами


# Основные эндпоинты

### Список товаров

```commandline
https://api.alimmah.dev/api/items/
```


### Детальная страница товара
```commandline
https://api.alimmah.dev/api/items/1/
```
### На странице товара:

- отображается информация о товаре

- тображается скидка (если есть)

- доступна покупка одного товара через Stripe Checkout


### Оплата заказа через Stripe
```commandline
path("orders/<int:pk>/buy/", OrderBuyAPIView.as_view(), name="order-buy")
```
Используется на странице заказов.

После нажатия кнопки Pay пользователь перенаправляется
на страницу оплаты Stripe Checkout.


# Архитектура проекта

- Item — товар

- Discount — скидка

- Order — заказ

- OrderItem — товар в заказе

- Stripe Checkout Session создаётся:

- для одного товара

- для всего заказа


## Тестирование оплаты (Stripe)
### Используйте тестовую карту Stripe:
```commandline
4242 4242 4242 4242
```

- Любая будущая дата
- Любой CVC

