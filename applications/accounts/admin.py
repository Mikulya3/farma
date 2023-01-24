from django.contrib import admin

from applications.accounts.models import CustomUser

admin.site.register(CustomUser)
