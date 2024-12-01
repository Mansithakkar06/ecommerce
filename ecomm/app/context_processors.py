from .models import Category
from .models import Cart

def categories_processor(request):
    return {'categories': Category.objects.all()}

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
            if cart:
                count = sum(item.quantity for item in cart.cartproduct_set.all())
    return {'cart_count': count}

