from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'amount']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)




