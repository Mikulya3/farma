from rest_framework import serializers
from .models import Category, Product
from .tasks import send_confirmation_email


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'image']

from rest_framework import serializers

from applications.product.models import Payment, Order, OrderItem


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        amount = validated_data['amount']
        product = validated_data['product']
        if amount > product.amount:
            raise serializers.ValidationError('no such amount!')
        if amount == 0:
            raise serializers.ValidationError('necessary to order one product')

        product.amount -= amount
        product.save(update_fields=['amount'])

        order = Order.objects.create(**validated_data)
        send_confirmation_email(order.title.email, order.activation_code, order.product.amount, order.price)
        return order

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity']



