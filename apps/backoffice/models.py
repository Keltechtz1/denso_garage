from django.db import models
# Create your models here.
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import datetime
from django.contrib.auth.models import User
from django.utils.html import mark_safe

from django.dispatch import receiver
from django.db.models.signals import post_save

from django.db import models

from django.utils.timezone import now
from datetime import datetime

from django.utils.html import mark_safe
import datetime
from  apps.workshop.models import Customer, Department


class UserProfile(models.Model):
	USER_TYPE = (
		('Admin', 'Admin'),
		('Staff', 'Staff'),
		('Procurement', 'Procurement'),
		('Accountant', 'Accountant'),
		
	)



	GENDER = (
		('Male','Male'),
		('Female', 'Female'),
	)

	user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
	phone = models.CharField(max_length=255, help_text='Eg 0755..')
	region = models.CharField(max_length=255, help_text='Eg Dar Es Salaam]')
	address = models.CharField(max_length=255,help_text='Your address info...')
	bio = RichTextUploadingField(blank=True, null=True,  help_text=' bio... ')
	role = models.CharField(max_length=20, choices=USER_TYPE, default='Staff')
	gender = models.CharField(max_length=20, choices=GENDER, blank=True)
	photo = models.ImageField(upload_to='profiles', default='avatar.png')
	is_online = models.BooleanField(default=False)
	class Meta:
		verbose_name_plural = 'User Profiles'
	def __str__(self):
		return str(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='Staff')


class Service(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique=True)
	about_service = RichTextUploadingField(blank=True, null=True,  help_text=' about the service ... ')
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add =True)
	class Meta:
		verbose_name_plural = 'Services'
	def __str__(self):
 		return str(self.title)



class CustomerOrders(models.Model):
 	PAYMENT_METHOD = ( ('Cash','Cash'), ('Credit', 'Credit'), )
 	PAYMENT_STATUS = ( ('Paid','Paid'), ('Unpaid', 'Unpaid'), )
 	WORK_STATUS = ( ('New Job','New Job' ) ,('Job completed not paid','Job completed not paid'), ('Job paid not completed', 'Job paid not completed'),('Job paid completed', 'Job paid completed'),('Canceled', 'Canceled'))
 	CURRENCE_TYPE = ( ('TZS','TZS'), ('USD', 'USD'),)
 	customer = models.ForeignKey(Customer,related_name='customerorder', on_delete=models.CASCADE)
 	car_name = models.CharField(max_length=255, help_text='Eg Toyota Land Cruiser ...')
 	plate_no = models.CharField(max_length=255,blank=False, null=False, help_text='Eg  D200 TZ ...')
 	model_no = models.CharField(max_length=255,blank=True, null=True, help_text='car model ...')
 	chassis_no = models.CharField(max_length=255,blank=True, null=True, help_text='car Chassis Number ...', default='')
 	number_of_km = models.CharField(max_length=255,blank=True, null=True, help_text='car km ...', default='0')
 	problem_statement = RichTextUploadingField(blank=False, null=False,  help_text=' bio... ')
 	payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD, default='Cash')
 	payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS, default='Unpaid')
 	work_status = models.CharField(max_length=30, choices=WORK_STATUS, default='New Job')
 	department = models.ManyToManyField(Department,default='1')
 	service_by = models.CharField(max_length=255, help_text='Staff name', null=False, blank=False,default='')
 	arrival_date = models.DateTimeField(auto_now_add =True)
 	departure_date = models.DateField(blank=True, null=True)
 	updated_at = models.DateTimeField(auto_now=True)
 	class Meta:
 		verbose_name_plural = 'Customer Order'
 	def __str__(self):
 		return str(self.customer.customer_name)

 	@property
 	def total_amount(self):
 		details = CustomerOrderDetail.objects.filter(order_id=self.id)
 		total_cost  = 0
 		for item in details:
 			total = item.quantity * item.amount
 			total_cost += total
 		return total_cost

 	@property
 	def order_items(self):
 		items = CustomerOrderDetail.objects.filter(order_id=self.id)
 		return items


	


class CustomerOrderDetail(models.Model):
	AVAILABILITY = ( ('Waiting','Waiting'), ('Available','Available'), ('Unavailable', 'Unavailable'),('Dispatched','Dispatched'))
	ITEM_STATUS = ( ('Delivered','Delivered'), ('Not Delivered','Not Delivered'),( 'Received','Received'))
	order_id = models.ForeignKey(CustomerOrders,related_name='order_id', on_delete=models.CASCADE)
	item = models.CharField(max_length=255)
	unit = models.CharField(max_length=255, blank=True, null=True, help_text='Eg: PC, UNIT...')
	amount = models.DecimalField(max_digits=65, decimal_places=2, default=0)
	quantity = models.IntegerField(default=1)
	contractor = models.CharField(max_length=255, blank=True, null=True)
	parts_no = models.CharField(max_length=255, blank=True, null=True, default='')
	work_status = models.CharField(max_length=30, choices=AVAILABILITY, default='Waiting')
	item_status = models.CharField(max_length=30, choices=ITEM_STATUS, default='Not Delivered')
	added_date = models.DateTimeField(auto_now_add =True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		verbose_name_plural = 'Order Details'
	def __str__(self):
		return  '{0} ({1})'.format(self.order_id,self.item)
	@property
	def total_amount(self):
		return (self.quantity * self.amount)


class Vendor(models.Model):
	vendor_name = models.CharField(max_length=255, blank=False,help_text='enter vendor name ...')
	vendor_email = models.CharField(max_length=255, blank=True, null=True,help_text='enter vendor email ...')
	vendor_phone = models.CharField(max_length=255, blank=False,null=False, help_text='enter vendor phone..')
	vendor_address = models.CharField(max_length=255, blank=True,null=True, help_text='vendor address...')
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add =True)

	@property
	def vrequests(self):
		vrequests = VendorOrders.objects.filter(vendor=self.id)
		return vrequests

	class Meta:
		verbose_name_plural = 'Customers '
	def __str__(self):
		return  '{0} ({1})'.format(self.vendor_name,self.vendor_phone)


class VendorOrders(models.Model):
 	PAYMENT_STATUS = ( ('Paid','Paid'), ('Unpaid', 'Unpaid'), )
 	WORK_STATUS = ( ('Pending','Pending'), ('Approved', 'Approved'), ('Denied', 'Denied'), ('Canceled', 'Canceled',))
 	REQUEST_TYPE = ( ('Technical services','Technical services'), ('Purchases', 'Purchases'),)
 	PAYMENT_METHOD = ( ('Cash','Cash'), ('Credit', 'Credit'),)
 	vendor = models.ForeignKey(Vendor,related_name='vorder', on_delete=models.CASCADE)
 	order_type = models.CharField(max_length=30, choices=REQUEST_TYPE, default='Technical services')
 	title = models.CharField(max_length=255, help_text='Eg ufundi ...', default='')
 	description = RichTextUploadingField(blank=False, null=False,  help_text=' bio... ', default='')
 	payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS, default='Unpaid')
 	payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD, default='Cash')
 	work_status = models.CharField(max_length=30, choices=WORK_STATUS, default='Pending')
 	start_date = models.DateTimeField(auto_now_add =True)
 	end_date = models.DateField(blank=True, null=True)
 	updated_at = models.DateTimeField(auto_now=True)
 	class Meta:
 		verbose_name_plural = 'Outsource Order'
 	def __str__(self):
 		return str(self.customer)

 	@property
 	def total_amount(self):
 		details = VendorOrderDetail.objects.filter(order_id=self.id)
 		total_cost  = 0
 		for item in details:
 			total = item.quantity * item.amount
 			total_cost += total
 		return total_cost

 	@property
 	def order_items(self):
 		items = VendorOrderDetail.objects.filter(order_id=self.id)
 		return items

 	@property
 	def comments(self):
 		comments = VendorOrderComment.objects.filter(order=self.id).order_by('-post_date')
 		return comments


class VendorOrderDetail(models.Model):
	WORK_STATUS = ( ('Waiting','Waiting'), ('On Progress', 'On Progress'), ('Completed', 'Completed'), ('Canceled', 'Canceled',))
	order_id = models.ForeignKey(VendorOrders,related_name='order_id', on_delete=models.CASCADE)
	item = models.CharField(max_length=255)
	unit = models.CharField(max_length=255, blank=True, null=True, help_text='Eg: PC, UNIt...')
	amount = models.DecimalField(max_digits=65, decimal_places=2, default=0)
	quantity = models.IntegerField(default=1)
	work_status = models.CharField(max_length=30, choices=WORK_STATUS, default='Waiting')
	added_date = models.DateTimeField(auto_now_add =True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		verbose_name_plural = 'Order Details'
	def __str__(self):
		return  '{0} ({1})'.format(self.order_id,self.item)
	@property
	def total_amount(self):
		return (self.quantity * self.amount)


class VendorOrderComment(models.Model):
	order = models.ForeignKey(VendorOrders,related_name='chat_order', on_delete=models.CASCADE)
	staff = models.ForeignKey(User, related_name='staff', on_delete=models.CASCADE)
	comment = models.TextField(blank=False, null=False)
	post_date = models.DateTimeField(auto_now_add =True)

	class Meta:
		verbose_name_plural = 'Vendor Comments'

	def __str__(self):
		return str(self.order)
	


