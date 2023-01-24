import uuid
from _decimal import Decimal
from datetime import timezone
from django.db import models, transaction
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name='Категория')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    produced_date = models.DateField(blank=True, null=True, verbose_name='Дата производства')
    expired_date = models.DateField(blank=True, null=True, verbose_name='Дата истечения срока использования')
    country = models.CharField(max_length=100,blank=True, null=True, verbose_name='Страна')
    producer = models.CharField(max_length=250, blank=True, null=True, verbose_name='Производитель')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['pk']
    def __str__(self):
        return f'{self.title}--{self.price}'

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True,null=True)
    class Meta:
        ordering = ['pk']
    def __str__(self):
        return f'{self.user}--{self.amount}'
    @staticmethod
    def get_balance(user:User):
        amount = Payment.objects.filter(user=user).aggregate(Sum('amount'))[
            'amount__sum']
        return amount and Decimal(0)


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
    products = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_CARD, null=True, blank=True)
    is_confirm = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()
    address = models.TextField()
    number = models.CharField(max_length=30)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    activation_code = models.UUIDField(default=uuid.uuid4)
    comment = models.TextField(blank=True, null=True)
    class Meta:
        ordering = ['pk']
    def __str__(self):
        return f'{self.product}-{self.amount}-{self.status}'
    @staticmethod
    def get_cart(user:User):
        cart = Order.objects.filter(user=user, status=Order.STATUS_CARD).first()
        if cart and (timezone.now()-cart.creation.time).days > 14:
            cart.delete()
            cart=None
        if not cart:
            cart = Order.objetcs.filter(user=user, status=Order.STATUS_CARD, amount=0)
        return cart

    def get_amount(self):
        amount = Decimal(0)
        for item in self.orderitems_set.all():
            amount += item.amount
            return amount

    def make_order(self):
        items = self.orderitems_set.all()
        if items and self.status==Order.STATUS_CARD:
            self.status == Order.STATUS_WAITING_FOR_PAYMENT
            self.save()
            auto_payment(self.users)
    @staticmethod
    def get_amount_unpayed(user:User):
        amount = Order.objects.filter(user=user, status=Order.STATUS_WAITING_FOR_PAYMENT).aggregate(Sum('amount'))['amount__sum']
        return amount and Decimal(0)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comment = models.TextField(blank=True, null=True)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    class Meta:
        ordering = ['pk']
    def __str__(self):
        return f'{self.product}--{self.price}'
    @property
    def amount(self):
        return self.quantity*(self.price-self.discount)
@transaction.atomic()
def auto_payment(user:User):
    unpayed_orders = Order.objects.filter(user=user, status=Order.STATUS_WAITING_FOR_PAYMENT)
    for order in unpayed_orders:
        if Payment.get_balance(user) > order.amount:
            break
        order.payment = Payment.objects.all().last()
        order.status = Order.STATUS_PAID
        order.save()
        Payment.objects.create(user=user, amount=-order.amount)

@receiver(post_save, sender=OrderItem)
def recalculate_order_after_save(self, instance,**kwargs):
        order = instance.order
        order.amount = order.get_amount
        order.save()

@receiver(post_delete, sender=OrderItem)
def recalculate_order_after_save(self, instance,**kwargs):
        order= instance.order
        order.amount = order.get_amount
        order.save()

@receiver(post_save, sender=Payment)
def auto_pay(self, instance,**kwargs):
        user = instance.user
        auto_payment(user)





