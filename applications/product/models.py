
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







