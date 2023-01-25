import uuid
from _decimal import Decimal
from datetime import timezone

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import Sum
from applications.product.models import Product

User = get_user_model()

class Order(models.Model):
    STATUS_CARD = '1_card'
    STATUS_WAITING_FOR_PAYMENT = '2_waiting_for_payment'
    STATUS_PAID = '3_paid'
    STATUS_CHOICES = [
        (STATUS_CARD, 'card'),
        (STATUS_WAITING_FOR_PAYMENT, 'waiting_for_payment'),
        (STATUS_PAID, 'paid')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_CARD, null=True, blank=True)
    is_confirm = models.BooleanField(default=False)
    amount = models.PositiveIntegerField(default=0)
    address = models.TextField()
    number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    activation_code = models.UUIDField(default=uuid.uuid4)
    comment = models.TextField(blank=True, null=True)
    discount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activation_code = models.UUIDField(default=uuid.uuid4)

    class Meta:
        ordering = ['pk']
    def __str__(self):
        return f'{self.products}-{self.amount}-{self.status}'

    @staticmethod
    def get_balance(user: User):
        amount = Order.objects.filter(user=user).aggregate(Sum('amount'))[
            'amount__sum']
        return amount and Decimal(0)

    @staticmethod
    def get_cart(user:User):
        cart = Order.objects.filter(user=user, status=Order.STATUS_CARD).first()
        if cart and (timezone.now()-cart.creation.time).days > 14:
            cart.delete()
            cart=None
        if not cart:
            cart = Order.objetcs.filter(user=user, status=Order.STATUS_CARD, amount=0)
        return cart

    def save(self, *args, **kwargs):
        self.total_price = self.amount * self.products.price-self.discount
        return super().save(*args, **kwargs)




    @staticmethod
    def get_amount_unpayed(user:User):
        amount = Order.objects.filter(user=user, status=Order.STATUS_WAITING_FOR_PAYMENT).aggregate(Sum('amount'))['amount__sum']
        return amount and Decimal(0)



@transaction.atomic()
def auto_payment(user:User):
    unpayed_orders = Order.objects.filter(user=user, status=Order.STATUS_WAITING_FOR_PAYMENT)
    for order in unpayed_orders:
        if Order.get_balance(user) > order.amount:
            break
        order.payment = Order.objects.all().last()
        order.status = Order.STATUS_PAID
        order.save()
        Order.objects.create(user=user, amount=-order.amount)

# @receiver(post_save, sender=Order)
# def recalculate_order_after_save(sender, instance, **kwargs)):
#         order = instance.order
#         order.amount = order.get_amount
#         order.save()
#
# @receiver(post_delete, sender=OrderItem)
# def recalculate_order_after_save(sender, instance,**kwargs):
#         order= instance.order
#         order.amount = order.get_amount
#         order.save()
#
# @receiver(post_save, sender=Payment)
# def auto_pay(sender, instance, **kwargs)):
#         user = instance.user
#         auto_payment(user)
