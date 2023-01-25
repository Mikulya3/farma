from django.contrib import admin

from applications.oder.models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'owner', 'products', 'total_price', 'amount']


admin.site.register(Order, OrderAdmin)