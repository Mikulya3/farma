import uuid
from django.contrib.auth import get_user_model
from django.db import models
from applications.product.models import Product

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True,null=True)

class Order(models.Model):
    STATUS_CARD = '1_card'
    STATUS_WAITING_FOR_PAYMENT = '2_waiting_for_payment'
    STATUS_PAID = '3_paid'
    STATUS_CHOICES = [
        (STATUS_CARD, 'card'),
        (STATUS_WAITING_FOR_PAYMENT, 'waiting_for_payment'),
        (STATUS_PAID, 'paid')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_CARD, null=True, blank=True)
    is_confirm = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()
    address = models.TextField()
    number = models.CharField(max_length=30)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    activation_code = models.UUIDField(default=uuid.uuid4)
    comment = models.TextField(blank=True, null=True)

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comment = models.TextField(blank=True, null=True)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

