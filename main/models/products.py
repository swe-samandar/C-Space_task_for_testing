from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

