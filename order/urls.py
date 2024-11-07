from django.urls import path
from .views import CartPage

app_name = 'order'

urlpatterns = [
    path('cart/', CartPage.as_view(), name='cart'),
]
