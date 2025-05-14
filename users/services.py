import stripe
import json
import requests
import math

from config.settings import STRIPE_API_KEY

# Ключ Stripe
stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создаем продукт в Stripe"""
    return stripe.Product.create(name=product)


def conversion_rub_into_usd(amount_rub):
    """Функция перевода рублей в USD."""
    # Получение курса валют с официального сайта ЦБ РФ
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)

    # Парсинг JSON ответа
    data = json.loads(response.text)

    # Извлечение курса рубля к доллару
    rate = data['Valute']['USD']['Value']

    # Перевод суммы в рублях в сумму в долларах
    rubles = amount_rub
    usd_amount = rubles / rate

    return math.floor(usd_amount * 100) / 100


def create_stripe_price(amount_usd, stripe_product):
    """Создание цены в сервисе Stripe в USD."""
    return stripe.Price.create(
        currency="usd",
        unit_amount=int(amount_usd) * 100,
        product_data={"name": stripe_product['name']},
    )


def create_stripe_session(stripe_price):
    """Создание сессии в stripe."""
    # print(stripe_product['name'])
    session = stripe.checkout.Session.create(
        # Перенаправляем после покупки на главную страницу
        success_url="http://127.0.0.1:8000/course/",
        # Устанавливаем цену и количество покупаемого продукта
        line_items=[{"price": stripe_price.get('id'), "quantity": 1}],
        mode='payment',
    )
    return session.get('id'), session.get('url')


def checking_status_payment(id_session):
    """Проверка статуса оплаты"""
    payment_status = stripe.checkout.Session.retrieve(id_session,)
    return payment_status['payment_status']