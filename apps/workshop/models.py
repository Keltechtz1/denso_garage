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


class Department(models.Model):
	name = models.CharField(max_length=255, help_text='Eg : MECHANICAL')
	slug = models.SlugField(max_length=255, unique=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add =True)
	class Meta:
		verbose_name_plural = 'Departments'
	def __str__(self):
 		return str(self.name)


class Customer(models.Model):
	customer_name = models.CharField(max_length=255, blank=False,help_text='enter customer name ...')
	customer_email = models.CharField(max_length=255, blank=True, null=True,help_text='enter customer email ...')
	customer_phone = models.CharField(max_length=255, blank=False,null=False, help_text='enter customer phone..')
	driver_name = models.CharField(max_length=255, blank=True,null=True, help_text='Drive Name...', default='')
	driver_phone = models.CharField(max_length=255, blank=False,null=False, help_text='enter phone..', default='')
	customer_address = models.CharField(max_length=255, blank=True,null=True, help_text='customer address...')
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add =True)
	class Meta:
		verbose_name_plural = 'Customers '
	def __str__(self):
		return  '{0} ({1})'.format(self.customer_name,self.driver_name)

class Requisition(models.Model):
	name = models.CharField(max_length=255, blank=False,help_text=' name ...')
	make = models.CharField(max_length=255, blank=False,help_text='make  ...')
	requisition_from = models.CharField(max_length=255, blank=False,help_text='from  ...')
	requisition_to = models.CharField(max_length=255, blank=False,help_text='to  ...')
	request_by = models.ForeignKey(User,related_name='request_by', on_delete=models.CASCADE)
	issued_by = models.ForeignKey(User,related_name='issued', on_delete=models.CASCADE, blank=True, null=True)
	authorized_by = models.ForeignKey(User,related_name='authorized_by', on_delete=models.CASCADE, blank=True, null=True)	
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add =True)
	class Meta:
		verbose_name_plural = 'Requisitions '
	def __str__(self):
		return  '{0} ({1})'.format(self.name,self.make)

	@property
	def ritems(self):
		items = RequisitionDetails.objects.filter(requisition=self.id)
		return items
	@property
	def total_amount(self):
		details = RequisitionDetails.objects.filter(requisition=self.id)
		total_cost  = 0
		for item in details:
			total = item.quantity * item.remarks
			total_cost += total
		return total_cost


class RequisitionDetails(models.Model):
	requisition = models.ForeignKey(Requisition,related_name='requisition', on_delete=models.CASCADE)
	item = models.CharField(max_length=255)
	supplier = models.CharField(max_length=255, blank=True, null=True)
	unit = models.CharField(max_length=255, blank=True, null=True, help_text='Eg: PC, UNIT...')
	quantity = models.IntegerField(default=1)
	remarks = models.DecimalField(max_digits=65, decimal_places=2, default=0)
	hq_feedback = models.CharField(max_length=255, blank=True, null=True, default='')
	added_date = models.DateTimeField(auto_now_add =True)
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		verbose_name_plural = 'Requisition Details'
	def __str__(self):
		return  '{0} ({1})'.format(self.requisition,self.item)
	@property
	def total_amount(self):
		return (self.quantity * self.remarks)


