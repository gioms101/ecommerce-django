from django.db.models import Sum
from .models import Category
from order.models import CartItem


def product_count(request):
    user = request.user
    products = CartItem.objects.filter(cart_id=user.id).aggregate(product_count=Sum('quantity'))
    return {'product_count': products['product_count']}


def get_parent_categories(request):
    parent_categories = Category.objects.filter(parent_id=None)
    return {"parent_categories": parent_categories}
