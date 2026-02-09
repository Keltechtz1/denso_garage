from django.shortcuts import render, redirect,get_object_or_404

# Create your views here.
from django.http import HttpResponse,HttpResponseNotFound,Http404,JsonResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
# change password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.db.models import Sum
#send mail


from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import get_template
from io import BytesIO

# for pdf
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

 
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from django.db.models import Sum
from django.template.defaultfilters import slugify


# Create your views here.
from .forms import * 
from apps.workshop.forms import *		
from .models import *
from apps.workshop.models import *


@login_required
def office_dashboard(request):

  
  context = {
    'page' : 'dashboard',
	  'page_title' : 'HQ - Dashoard',
    'new_requests' : CustomerOrders.objects.filter(work_status='Job completed not paid').count(),
    'active' : CustomerOrders.objects.filter(work_status='Job paid not completed').count(),
    'completed' : CustomerOrders.objects.filter(work_status='Job paid completed').count(),
    'canceled' : CustomerOrders.objects.filter(work_status='Canceled').count(),
    'new_job' : CustomerOrders.objects.filter(work_status='New Job').count(),
    'paid' : CustomerOrders.objects.filter(payment_status='Paid').count(),
    'profoma' : CustomerOrders.objects.filter(payment_status='Unpaid').count(),
    'orders' : CustomerOrders.objects.filter(work_status='New Job'),

	  
  }

  return render(request,'backoffice/dashboard.html',context)


@login_required
def staff_view(request):
	context = {
		'page' : 'dashboard',
		'page_title' : 'Backoffice - Dashoard',
		# 'companies_no': User_Profile.objects.filter(user_type='Customer').count(),
	
	}
	return render(request,'backoffice/dashboard.html',context)


@login_required
def allOrderView(request):
  context = {
      'page' : 'orders',
      'main_page' : 'orders',
      'page_title'  : 'Customer Orders',
      'orders': CustomerOrders.objects.all().order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.all().count(),

  }
  return render(request,'backoffice/orders.html',context)



@login_required
def newOrderView(request):
  context = {
      'page' : 'new_order',
      'main_page' : 'orders',
      'page_title'  : 'Job Completed Not Paid',
      'orders': CustomerOrders.objects.filter(work_status='Job completed not paid').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='Job completed not paid').count(),

  }

  return render(request,'backoffice/orders.html',context)


@login_required
def activeWorkView(request):
  context = {
      'page' : 'active_work',
      'main_page' : 'orders',
      'page_title'  : 'Job Paid Not Completed',
      'orders': CustomerOrders.objects.filter(work_status='Job Paid Not Completed').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='JJob Paid Not Completed').count(),

  }
  return render(request,'backoffice/orders.html',context)

@login_required
def completedWorkView(request):
  context = {
      'page' : 'completed_work',
      'main_page' : 'orders',
      'page_title'  : 'Job Paid Completed',
      'orders': CustomerOrders.objects.filter(work_status='Job paid completed').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='Job paid completed').count(),

  }

  return render(request,'backoffice/orders.html',context)

@login_required
def canceledWorkView(request):
  context = {
      'page' : 'canceled_work',
      'main_page' : 'orders',
      'page_title'  : 'Canceled Works',
      'orders': CustomerOrders.objects.filter(work_status='Canceled').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='Canceled').count(),

  }

  return render(request,'backoffice/orders.html',context)

@login_required
def newJobView(request):
  context = {
      'page' : 'new_job',
      'main_page' : 'orders',
      'page_title'  : 'New Job',
      'orders': CustomerOrders.objects.filter(work_status='New Job').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='New Job').count(),

  }

  return render(request,'backoffice/orders.html',context)

@login_required
def paidInvoicesView(request):
  context = {
      'page' : 'paid',
      'main_page' : 'invoices',
      'page_title'  : 'Paid  Invoices',
      'orders': CustomerOrders.objects.filter(payment_status='Paid').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(payment_status='Paid').count(),

  }

  return render(request,'backoffice/invoices.html',context)




@login_required
def unpaidInvoicesView(request):
  context = {
      'page' : 'unpaid',
      'main_page' : 'invoices',
      'page_title'  : 'Unpaid  Invoices',
      'orders': CustomerOrders.objects.filter(payment_status='Unpaid').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(payment_status='Unpaid').count(),

  }

  return render(request,'backoffice/invoices.html',context)


@login_required
def previewInvoice(request, inv):
  order  = get_object_or_404(CustomerOrders, id=inv)
  context = {
      'page' : 'invoices',
      'main_page' : 'invoices',
      'page_title'  : 'preview invoice inv-'+str(order.id),
      'order': order,

  }
  return render(request,'backoffice/invoice_preview.html',context)
  
@login_required
def invoicePrint(request, inv):
  order  = get_object_or_404(CustomerOrders, id=inv)
  context = {
      'page' : 'invoices',
      'main_page' : 'invoices',
      'page_title'  : 'preview invoice inv-'+str(order.id),
      'order': order,

  }
  return render(request,'backoffice/printable_invoice.html',context)


@login_required
def delete_order(request, order):
  try:
    sub = get_object_or_404(CustomerOrders,id=order)
    sub.delete()
    messages.success(request, 'Order deleted successfully')
    return redirect('office:orders')
  except:
    messages.warning(request, 'Hmm..., the order not found!.')
    return redirect('office:orders')




@login_required
def customerView(request):
  context = {
      'page' : 'customers',
      'main_page' : 'customers',
      'page_title'  : 'All Customers',
      'customers': Customer.objects.all().order_by('-created_at')
  }

  return render(request,'backoffice/customers.html',context)




@login_required
def ordersView(request, customer):
	customer = Customer.objects.get(id=customer)
	orders = CustomerOrders.objects.filter(customer=customer)
	context = {
    'main_page' : 'orders',
    'page' : 'manage_order',
	  'page_title' : customer.customer_name+' Services',
	  'recents': Customer.objects.all().order_by('-created_at')[:10:1],
	  'customer': customer,
	  'orders': orders,
  }
	return render(request,'backoffice/customer_services.html',context)




@login_required
def update_order(request, order):
  order = CustomerOrders.objects.get(id=order)
  form = ManageOrderForm(instance=order)
  if request.method == "POST":
    form = ManageOrderForm(request.POST,instance=order)
    if form.is_valid(): 
      orderform = form.save(commit=False)
      orderform.save()
      messages.info(request, 'Order Updated successfully!')
      return redirect('office:update_order', order.id)
  context = {
    'main_page' : 'orders',
    'page' : 'manage_order',
    'page_title' : 'Update Order',
    'order': order,
      'form': form,
  }

  return render(request,'backoffice/order_management.html',context)



@login_required
def order_detail(request, order):
  order = CustomerOrders.objects.get(id=order)
  details = CustomerOrderDetail.objects.filter(order_id=order)
  form = ManageOrderDetailForm()
  if request.method == "POST":
    form = ManageOrderDetailForm(request.POST)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.order_id = order
      detailform.save()
      messages.success(request, 'item added successfully!')
      return redirect('office:order_detail', order.id)
  context = {
    'page' : 'orders',
    'main_page' : 'orders',
    'page_title' : 'Order Details',
    'order': order,
    'form': form,
    'details': details
  }

  return render(request,'backoffice/order_details.html',context)		



@login_required
def updateItem(request, order, item):
  order = CustomerOrders.objects.get(id=order)
  details = CustomerOrderDetail.objects.filter(order_id=order)
  item = get_object_or_404(CustomerOrderDetail, id=item)

  form = ManageOrderDetailForm(instance=item)
  if request.method == "POST":
    form = ManageOrderDetailForm(request.POST, instance=item)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.order_id = order
      detailform.save()
      messages.success(request, 'item updated successfully!')
      return redirect('office:order_detail', order.id)
  context = {
    'page' : 'orders',
    'main_page' : 'orders',
    'page_title' : 'Order Details',
    'order': order,
    'form': form,
    'details': details,
    'item': item
  }

  return render(request,'backoffice/order_details.html',context)		


@login_required
def addVendor(request):
  form = VendorForm()
  vendors = Vendor.objects.all().order_by('-created_at')
  if request.method == "POST":
    form = VendorForm(request.POST)
    if form.is_valid(): 
      vendorform = form.save(commit=False)
      vendorform.save()
      messages.success(request, vendorform.vendor_name+'  added successfully!')
      return redirect('office:add_vendor')
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Manage Vendor',
    'form': form,
    'vendors': vendors
  }

  return render(request,'backoffice/manage_vendor.html',context)  


@login_required
def updateVendor(request, vendor):
  vendor = get_object_or_404(Vendor, id=vendor)
  form = VendorForm(instance=vendor)
  vendors = Vendor.objects.all().order_by('-created_at')
  if request.method == "POST":
    form = VendorForm(request.POST, instance=vendor)
    if form.is_valid(): 
      vendorform = form.save(commit=False)
      vendorform.save()
      messages.success(request, vendorform.vendor_name+'  updated successfully!')
      return redirect('office:add_vendor')
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Manage Vendor',
    'form': form,
    'vendors': vendors
  }

  return render(request,'backoffice/manage_vendor.html',context)  






@login_required
def vendorInvoice(request, vendor):
  form = VendorOrderForm()
  vendor= get_object_or_404(Vendor, id=vendor)
  if request.method == "POST":
    form = VendorOrderForm(request.POST)
    if form.is_valid(): 
      invform = form.save(commit=False)
      invform.vendor = vendor
      invform.save()
      messages.success(request,'Invice created successfully!')
      return redirect('office:inv_detail',invform.id )
    else:
       messages.warning(request,form.errors)
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Invoice to '+vendor.vendor_name,
    'form': form,
    'vendor': vendor
  }

  return render(request,'backoffice/vendor_invoices.html',context)	



@login_required
def vendor_invoice_detail(request, order):
  order = VendorOrders.objects.get(id=order)
  details = VendorOrderDetail.objects.filter(order_id=order)
  form = VendorDetailForm()
  if request.method == "POST":
    form = VendorDetailForm(request.POST)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.order_id = order
      detailform.save()
      messages.success(request, 'item added successfully!')
      return redirect('office:inv_detail', order.id)
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Order Details',
    'order': order,
    'form': form,
    'details': details
  }

  return render(request,'backoffice/vendor_invoice_detail.html',context)    


@login_required
def UpdateVendorInvoice(request, vendor, order):
  order = get_object_or_404(VendorOrders, id=order)
  form = VendorOrderForm(instance=order)
  vendor= get_object_or_404(Vendor, id=vendor)
  
  if request.method == "POST":
    form = VendorOrderForm(request.POST, instance=order)
    if form.is_valid(): 
      invform = form.save(commit=False)
      invform.vendor = vendor
      invform.save()
      messages.success(request,'Order update successfully, sent to backoffice!')
      return redirect('office:inv_detail',invform.id )
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Invoice to '+vendor.vendor_name,
    'form': form,
    'vendor': vendor,
    'order' : order
  }

  return render(request,'backoffice/vendor_invoices.html',context)  

@login_required
def requestPreview(request, inv):
  order  = get_object_or_404(VendorOrders, id=inv)
  context = {
      'page' : 'requests',
      'main_page' : 'vendors',
      'page_title'  : 'preview request inv-'+str(order.id),
      'order': order,

  }
  return render(request,'backoffice/request_preview.html',context)


@login_required
def requestInvoicesView(request):
  context = {
      'page' : 'requests',
      'main_page' : 'vendors',
      'page_title'  : 'All Requests ',
      'orders': VendorOrders.objects.all().order_by('-id'),
      'all_in_no' : VendorOrders.objects.all().count(),

  }
  return render(request,'backoffice/all_requests.html',context)    


@login_required
def updateVendorItem(request, order, item):
  order = VendorOrders.objects.get(id=order)
  details = VendorOrderDetail.objects.filter(order_id=order)
  item = get_object_or_404(VendorOrderDetail, id=item)

  form = VendorDetailForm(instance=item)
  if request.method == "POST":
    form = VendorDetailForm(request.POST, instance=item)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.order_id = order
      detailform.save()
      messages.success(request, 'item updated successfully!')
      return redirect('office:inv_detail', order.id)
  context = {
    'page' : 'requests',
    'main_page' : 'vendors',
    'page_title' : 'Order Details',
    'order': order,
    'form': form,
    'details': details,
    'item': item
  }

  return render(request,'backoffice/vendor_invoice_detail.html',context)    


@login_required
def vendorComment(request, order):
  order = get_object_or_404(VendorOrders, id=order)
  if request.method == 'POST':
    comment = request.POST.get('comment','')
    newcomment = VendorOrderComment(order=order, staff=request.user, comment=comment) 
    newcomment.save()
    messages.success(request, 'Comment sent!')
    return redirect('office:inv_detail', order.id)
  else:
     messages.info(request, 'Comment not sent!')
     return redirect('office:inv_detail', order.id)
 



@login_required
def my_profile(request):
  if request.method == 'POST':
    request.user.first_name = request.POST.get('first_name','')
    request.user.last_name = request.POST.get('last_name','')
    request.user.email = request.POST.get('email','')
    request.user.profile.phone = request.POST.get('phone','')
    request.user.profile.region = request.POST.get('region','')
    request.user.profile.user_gender = request.POST.get('gender','')
    request.user.profile.address = request.POST.get('address','')
    request.user.profile.bio = request.POST.get('bio','')
    if len(request.FILES) != 0:
      myfile = request.FILES['photo']
      fs = FileSystemStorage()
      request.user.profile.photo = fs.save(myfile.name, myfile)
      uploaded_file_url = fs.url(request.user.profile.photo)

    request.user.save()
    request.user.profile.save()
    messages.success(request, 'profile updated successfuly!')
  

    return redirect('office:my_profile')
  context = {
    'page' : 'profile',
    'page_title' : str(request.user.username)+'\' profile',
   
    
  }
  return render(request,'backoffice/my_profile.html',context)



@login_required
def allRequisition(request):
  requisitions = Requisition.objects.all().order_by('-updated_at')
  context = {
    'page' : 'manage_requisition',
    'main_page' : 'requisitions',
    'page_title' : 'All Requisitions',
    'requisitions': requisitions
  }
  return render(request,'backoffice/requisitions.html',context)

@login_required
def updateRequisition(request,requisition):
  req = get_object_or_404(Requisition, id=requisition)
  form = RequisitionForm(instance=req)
  requisitions = Requisition.objects.filter(request_by=request.user).order_by('-created_at')
  if request.method == "POST":
    form = RequisitionForm(request.POST, instance=req)
    if form.is_valid(): 
     form = form.save(commit=False)
     form.request_by = request.user
     form.save()
     messages.success(request, 'Requisition update successfully!')
     return redirect('office:update_requisition', req.id)
  context = {
    'page' : 'manage_requisition',
    'main_page' : 'requisitions',
    'page_title' : 'Update Requisition',
    'form': form,
    'requisitions': requisitions
  }

  return render(request,'backoffice/manage_requisition.html',context)  


@login_required
def requisitionDetails(request, requisition):
  order = Requisition.objects.get(id=requisition)
  details = RequisitionDetails.objects.filter(requisition=order)
  form = HQRequisitionDetailsForm()
  if request.method == "POST":
    form = HQRequisitionDetailsForm(request.POST)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.requisition = order
      detailform.save()
      messages.success(request, 'item added successfully!')
      return redirect('office:requisition_details', order.id)
  context = {
    'page' : 'manage_requisition',
    'main_page' : 'requisitions',
    'page_title' : 'Requisition Details',
    'order': order,
    'form': form,
    'details': details
  }

  return render(request,'backoffice/requisition_details.html',context)    


@login_required
def updateRequisitionItem(request, requisition, desc):
  order = Requisition.objects.get(id=requisition)
  desc = get_object_or_404(RequisitionDetails, id=desc, requisition=order)
  details = RequisitionDetails.objects.filter(requisition=order)
  form = HQRequisitionDetailsForm(instance=desc)
  if request.method == "POST":
    form = HQRequisitionDetailsForm(request.POST, instance=desc)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.requisition = order
      detailform.save()
      messages.success(request, 'item updated successfully!')
      return redirect('office:reqsupdate_item', order.id, desc.id)
  context = {
    'page' : 'manage_requisition',
    'main_page' : 'requisitions',
    'page_title' : 'Requisition Details',
    'order': order,
    'form': form,
    'details': details
  }

  return render(request,'backoffice/requisition_details.html',context)    



@login_required
def requisitionPrint(request, req):
  order  = get_object_or_404(Requisition, id=req)
  context = {
      'page' : 'Requisition',
      'main_page' : 'Requisition',
      'page_title'  : 'preview requisition inv-'+str(order.id),
      'order': order,

  }
  return render(request,'backoffice/printable_requisition.html',context)
