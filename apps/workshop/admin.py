from django.contrib import admin

# Register your models here.

from .models import *

@admin.register(Customer) 
class CustomerAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('customer_name','customer_phone','driver_name','created_at','updated_at')
    search_fields = ['customer_name','customer_phone','driver_name']


@admin.register(Requisition) 
class RequisitionAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('name','make','requisition_from','requisition_to','created_at','updated_at')
    search_fields = ['name','make','requisition_from','requisition_to']


@admin.register(RequisitionDetails) 
class RequisitionDetailsAdmin(admin.ModelAdmin):
    list_filter = ('added_date',)
    list_display = ('requisition','item','unit','remarks','quantity','total_amount','added_date')
    search_fields = ['requisition','item']


@admin.register(Department) 
class DepartmentAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('name','slug','created_at')
    search_fields = ['name',]
    prepopulated_fields = {'slug':('name',) } 