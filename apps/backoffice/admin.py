from django.contrib import admin

# Register your models here.
from . models import *

@admin.register(UserProfile) 
class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('role','gender')
    list_display = ('user','role','gender','phone','region','is_online')
    search_fields = ['region','user']
    actions = ['is_online']
    
    def is_online(self, request, queryset):
        queryset.update(active=True)


@admin.register(Service) 
class ServiceAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('title','slug','created_at')
    search_fields = ['title',]
    prepopulated_fields = {'slug':('title',) } 


@admin.register(CustomerOrders) 
class CustomerOrdersAdmin(admin.ModelAdmin):
    list_filter = ('arrival_date',)
    list_display = ('customer','car_name','plate_no','model_no','chassis_no','number_of_km','arrival_date','departure_date')
    search_fields = ['customer','car_name','plate_no','model_no','chassis_no']


@admin.register(CustomerOrderDetail) 
class CustomerOrderDetailAdmin(admin.ModelAdmin):
    list_filter = ('order_id','added_date')
    list_display = ('order_id','item','unit','amount','quantity','contractor','parts_no','total_amount','added_date')
    search_fields = ['order_id','item']


@admin.register(Vendor) 
class VendorAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('vendor_name','vendor_phone','vendor_address','created_at','updated_at')
    search_fields = ['vendor_name','vendor_phone',]



@admin.register(VendorOrders) 
class VendorOrdersAdmin(admin.ModelAdmin):
    list_filter = ('payment_status','work_status')
    list_display = ('id','vendor','title','total_amount','payment_status','work_status','start_date','end_date')
    search_fields = ['vendor','title','payment_status']


@admin.register(VendorOrderComment) 
class VendorOrderCommentAdmin(admin.ModelAdmin):
    list_filter = ('staff',)
    list_display = ('id','order','staff','post_date')
    search_fields = ['comment','order','staff']
