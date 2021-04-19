from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ("equipment_id","equipment_name","is_available")
    search_fields = ("equipment_id","equipment_name","is_available")

