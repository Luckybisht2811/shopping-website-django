# app/utils.py

from .models import Cart

def get_cart_amount(user):
    cart_items = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    shipping = 40 if cart_items.exists() else 0
    total = amount + shipping
    return cart_items, amount, shipping, total
