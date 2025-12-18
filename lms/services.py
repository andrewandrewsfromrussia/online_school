import stripe

from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEY

def create_stripe_product(name):

    """Создает продукт в Stripe."""

    product = stripe.Product.create(name=name)

    return product.get("id")

def create_stripe_price(amount, product_id):

    """Создает цену в Stripe."""

    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=product_id,
    )

    return price.get("id")

def create_stripe_session(price_id):

    """Создает сессию на оплату в Stripe."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")