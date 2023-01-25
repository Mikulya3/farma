from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications.oder.models import Order
from applications.oder.tasks import send_confirmation_email

User = get_user_model()
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        amount = validated_data['amount']
        product = validated_data['products']
        if amount > product.amount:
            raise serializers.ValidationError('no such amount!')
        if amount == 0:
            raise serializers.ValidationError('necessary to order one product')

        product.amount -= amount
        product.save(update_fields=['amount'])

        order = Order.objects.create(**validated_data)
        send_confirmation_email(order.title.email, order.activation_code, order.product.amount, order.price)
        return order
