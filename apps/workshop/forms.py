from django import forms
from ckeditor.widgets import CKEditorWidget
from django.forms import DateInput


from .models import *
from apps.backoffice.models import *

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['customer_name', 'customer_email', 'customer_phone','driver_name','driver_phone','customer_address']



class DateInput(forms.DateInput):
    input_type = "date" 
  
class OrderForm(forms.ModelForm):
    department = forms.ModelMultipleChoiceField(queryset=Department.objects.all(),widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomerOrders
        fields   = ['car_name','plate_no','model_no','chassis_no','number_of_km','problem_statement','department','service_by','departure_date', 'payment_status','payment_method','work_status']
       
        widgets  = {'departure_date' : DateInput(),   
        }

    



class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = CustomerOrderDetail
        fields   = ['item','parts_no','unit','amount','quantity','contractor', 'item_status']
       
        


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_email', 'vendor_phone','vendor_address']


class VendorOrderForm(forms.ModelForm):
    class Meta:
        model = VendorOrders
        fields   = ['order_type','title','description','payment_status','payment_method','work_status','end_date']
       
        widgets  = {'end_date' : DateInput(),   
        }



class VendorDetailForm(forms.ModelForm):
    class Meta:
        model = VendorOrderDetail
        fields   = ['item','unit','amount','quantity']
        

class RequisitionDetailsForm(forms.ModelForm):
    class Meta:
        model = VendorOrderDetail
        fields   = ['item','unit','amount','quantity']
   



class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields   = ['name','make','requisition_from','requisition_to']
       
        # widgets  = {'end_date' : DateInput(),   
        # }



class RequisitionDetailsForm(forms.ModelForm):
    class Meta:
        model = RequisitionDetails
        fields   = ['item','supplier','unit','quantity','remarks']
   