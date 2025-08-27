from django.db import models
from .users import CustomUser
from .products import Product

class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    @property
    def total_price(self):
        return sum(op.product.price * op.quantity for op in self.order_products.all())

    def __str__(self):
        return f"Order #{self.id}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name="order_products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'OrderProduct'
        verbose_name_plural = 'OrderProducts'