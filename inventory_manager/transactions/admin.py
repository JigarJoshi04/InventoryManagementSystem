from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.RequestModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ("request_id","equipment","requested_by_user")
    search_fields = ("request_id","equipment","requested_by_user")
