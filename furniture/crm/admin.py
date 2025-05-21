from django.contrib import admin
from crm.models import ElementProduct,TypeOperation

@admin.register(ElementProduct)
class ElementProductAdmin(admin.ModelAdmin):
    pass


@admin.register(TypeOperation)
class TypeOperation(admin.ModelAdmin):
    pass