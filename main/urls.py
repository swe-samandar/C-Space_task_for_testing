from django.urls import path
from .views import (
    ClientsListView,
    SignInView,
    ProductsListView,
    NewProductView,
    ProductDetailView,
    OrdersListView,
    NewOrderView,
    OrderDetailView,
)

urlpatterns = [
    path('clients-list', ClientsListView.as_view()),
    path('signin', SignInView.as_view()),
    path('products-list', ProductsListView.as_view()),
    path('new-product', NewProductView.as_view()),
    path('product-detail/<int:pk>', ProductDetailView.as_view()),
    path('orders-list', OrdersListView.as_view()),
    path('new-order', NewOrderView.as_view()),
    path('order-detail/<int:pk>', OrderDetailView.as_view()),
]