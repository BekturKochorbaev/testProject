from django.urls import path
from .views import ItemListView, ItemDetailView, ItemBuyAPIView, OrderListView, OrderBuyAPIView

urlpatterns = [
    path('items/', ItemListView.as_view(), name='item-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path("orders/<int:pk>/buy/", OrderBuyAPIView.as_view(), name="order-buy"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("items/<int:pk>/buy/", ItemBuyAPIView.as_view(), name="item-buy"),

]
