import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(name):
    """Создает продукт в системе Stripe"""
    product = stripe.Product.create(name=name)
    return product.id

def create_stripe_price(amount, product_id):
    """Создает цену для продукта в копейках (центах)"""
    price = stripe.Price.create(
        currency="rub",
        # Переводим сумму в копейки (умножаем на 100 и приводим к числу)
        unit_amount=int(amount * 100),
        product=product_id,
    )
    return price.id

def create_stripe_session(price_id):
    """Создает сессию оплаты Stripe и возвращает ID сессии и ссылку на оплату"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url

def retrieve_stripe_session(session_id):
    """Дополнительное задание: Получение данных о сессии по ее идентификатору"""
    session = stripe.checkout.Session.retrieve(session_id)
    return session.payment_status
