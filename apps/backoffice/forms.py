from django import forms
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from django.forms import DateInput


from .models import *
from apps.workshop.models import *  

class staffForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name','password']


class VendorForm(forms.ModelForm):
	class Meta:
		model = Vendor
		fields = ['vendor_name', 'vendor_email', 'vendor_phone','vendor_address']


class DateInput(forms.DateInput):
    input_type = "date" 
  
class VendorOrderForm(forms.ModelForm):
    class Meta:
        model = VendorOrders
        fields   = ['order_type','title','description','payment_status','payment_method','work_status','end_date']
       
        widgets  = {'end_date' : DateInput(),   }




class VendorDetailForm(forms.ModelForm):
    class Meta:
        model = VendorOrderDetail
        fields   = ['item','unit','amount','quantity']
       

class ManageOrderDetailForm(forms.ModelForm):
    class Meta:
        model = CustomerOrderDetail
        fields   = ['item','parts_no','unit','amount','quantity','contractor','work_status' ]


class ManageOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrders
        fields   = ['car_name','plate_no','model_no','chassis_no','number_of_km','problem_statement','payment_method','payment_status','work_status','departure_date']
       
        widgets  = {'departure_date' : DateInput(),   
        }



class HQRequisitionDetailsForm(forms.ModelForm):
    class Meta:
        model = RequisitionDetails
        fields   = ['item','supplier','unit','quantity','remarks', 'hq_feedback']
   