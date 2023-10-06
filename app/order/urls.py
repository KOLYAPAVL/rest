from django.urls import path
from .views import Cart, OrderDetail, Orders

urlpatterns = [
    path('cart', Cart.as_view(), name='cart'),
    path('order/<int:pk>', OrderDetail.as_view(), name='orderDetail'),
    path('orders', Orders.as_view(), name='orders'),
]
