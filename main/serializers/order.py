from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from main.models import Order, OrderProduct, Product


class OrderProductSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_title', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, source='order_products')

    class Meta:
        model = Order
        fields = ['id', 'client', 'total_price', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('order_products', [])
        created = False

        for product_data in products_data:
            product = product_data['product']
            qty = product_data['quantity']

            if product.quantity < qty:
                raise ValidationError(
                    {"product": f"Only {product.quantity} {product.title} left"}
                )

            if not created:
                order = Order.objects.create(**validated_data)
                created = True

            product.quantity -= qty
            product.save()

            OrderProduct.objects.create(order=order, **product_data)

        return order

    def update(self, instance, validated_data):
        products_data = validated_data.pop('order_products', [])

        instance.client = validated_data.get('client', instance.client)
        instance.save()

        for old_item in instance.order_products.all():
            product = old_item.product
            product.quantity += old_item.quantity
            product.save()

        instance.order_products.all().delete()

        for product_data in products_data:
            product = product_data['product']
            qty = product_data['quantity']

            if product.quantity < qty:
                raise ValidationError(
                    {"product": f"Only {product.quantity} {product.title} left"}
                )

            product.quantity -= qty
            product.save()

            OrderProduct.objects.create(order=instance, **product_data)

        return instance
