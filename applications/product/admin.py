from django.contrib import admin
from .models import Category, Product
from applications.product.models import Payment, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'amount']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)



