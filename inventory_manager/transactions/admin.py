from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.RequestModel)
class RequestModelAdmin(admin.ModelAdmin):
    list_display = ("request_id","equipment","requested_by_user")
    search_fields = ("request_id","equipment","requested_by_user")


@admin.register(models.LogModel)
class LogModelAdmin(admin.ModelAdmin):
    list_display = ("log_id","request_id","request_granted","equipment","requested_by_user", "actioned_by")
    search_fields = ("log_id","request_id","request_granted","equipment","requested_by_user", "actioned_by")



@admin.register(models.IssueBookModel)
class IssueBookModelAdmin(admin.ModelAdmin):
    list_display = ("issue_id","equipment","requested_by_user", "actioned_by")
    search_fields = ("issue_id","equipment","requested_by_user", "actioned_by")
