from django.contrib import admin
from applications.spam.models import Spam
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email']
admin.site.register(Spam,ContactAdmin)
