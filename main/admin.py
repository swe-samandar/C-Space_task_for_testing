from django.contrib import admin
from .models import CustomUser, Product, Order, OrderProduct

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']
    search_fields = ['username', 'email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'quantity']

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'total_price']
    inlines = [OrderProductInline]

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
