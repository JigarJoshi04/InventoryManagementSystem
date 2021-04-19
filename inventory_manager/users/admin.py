from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","phone_number","email", "is_manager", "password","is_staff", "is_superuser", "is_active")
    search_fields = ("first_name","last_name","phone_number","email", "is_manager", "password","is_staff", "is_superuser", "is_active")

