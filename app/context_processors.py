from .models import Cart

def cart_item_count(request):
    """
    Global context processor:
    - Navbar cart badge ke liye
    - Har page par automatic available
    """

    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_count = 0

    return {
        'cart_item_count': cart_count
    }
