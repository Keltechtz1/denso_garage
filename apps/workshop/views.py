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


from apps.backoffice.models import *
from .models import *
# Create your views here.
from .forms import *

from datetime import datetime


@login_required
def work_dashboard(request):
  form = CustomerForm()
  if request.method == "POST":
    form = CustomerForm(request.POST)
    if form.is_valid(): 
      customer_phone = form.cleaned_data['customer_phone']
      newclient = form.save(commit=False)
      if Customer.objects.filter(customer_phone=customer_phone):
        messages.warning(request, 'Customer with this number '+customer_phone+' is already registered!')
      else:
        newclient.save()
        order = CustomerOrders.objects.create(customer=newclient)
        order.save()
        messages.success(request, 'Customer registered success!')
        return redirect('work:orders', newclient.id)
  context = {
      'page' : 'dashboard',
	    'page_title' : 'Workshop - Dashoard',
	    'recents': Customer.objects.all().order_by('-created_at')[:10:1],
      'form': form,
      'in_review' : CustomerOrders.objects.filter(work_status='New Job').count(),
      'in_process' : CustomerOrders.objects.filter(work_status='In Process').count(),
      'completed' : CustomerOrders.objects.filter(work_status='Completed').count(),
      'completed_not_paid' : CustomerOrders.objects.filter(work_status='Job completed not paid').count(),
      'paid_not_completed' : CustomerOrders.objects.filter(work_status='Job paid not completed').count(),
      'paid_completed' :CustomerOrders.objects.filter(work_status='Job paid completed').count(),
      'paid' : CustomerOrders.objects.filter(payment_status='Paid').count(),
      'profoma' : CustomerOrders.objects.filter(payment_status='Unpaid').count(),
      'canceled' : CustomerOrders.objects.filter(work_status='Canceled').count(),

  }

  return render(request,'workshop/dashboard.html',context)


@login_required
def updateCustomer(request, customer):
  customer = get_object_or_404(Customer, id=customer)
  form = CustomerForm(instance=customer)
  if request.method == "POST":
    form = CustomerForm(request.POST, instance=customer)
    if form.is_valid(): 
      customer_phone = form.cleaned_data['customer_phone']
      newclient = form.save(commit=False)
      newclient.save()
      order = CustomerOrders.objects.create(customer=newclient)
      order.save()
      messages.success(request, 'Customer Updated successfully!')
      return redirect('work:update_customer', newclient.id)
  context = {
      'page' : 'dashboard',
    'page_title' : 'Workshop - Dashoard',
    'recents': Customer.objects.all().order_by('-created_at')[:10:1],
      'form': form,
  }

  return render(request,'workshop/dashboard.html',context)




@login_required
def customerView(request):
  context = {
      'page' : 'customers',
      'main_page' : 'customers',
      'page_title'  : 'All Customers',
      'customers': Customer.objects.all().order_by('-created_at')
  }

  return render(request,'workshop/customers.html',context)




@login_required
def invoiceView(request):
	orders = CustomerOrders.objects.all()
	context = {
    'page' : 'orders',
	  'page_title' : 'All Customer Order',
	  'orders': orders,
  }
	return render(request,'workshop/invoice.html',context)



@login_required
def ordersView(request, customer):
  customer = Customer.objects.get(id=customer)
  orders = CustomerOrders.objects.filter(customer=customer)
  context = {
      'page' : 'dashboard',
    'page_title' : customer.customer_name+' Services',
    'recents': Customer.objects.all().order_by('-created_at')[:10:1],
    'customer': customer,
    'orders': orders,
  }
  return render(request,'workshop/customer_services.html',context)

@login_required
def newService(request, customer):
  customer = Customer.objects.get(id=customer)
  orderform = None
  form = OrderForm()
  if request.method == "POST":
    form = OrderForm(request.POST)
    if form.is_valid(): 
      orderform = form.save(commit=False)
      orderform.customer = customer
      orderform.save()
      messages.info(request, 'Service placed successfully!')
      return redirect('work:order_detail', orderform.id)
  context = {
      'page' : 'dashboard',
    'page_title' : 'Workshop - Add Service',
    'order': orderform,
      'form': form,
  }

  return render(request,'workshop/order_management.html',context)




@login_required
def update_order(request, order):
  order = CustomerOrders.objects.get(id=order)
  form = OrderForm(instance=order)
  if request.method == "POST":
    form = OrderForm(request.POST,instance=order)
    if form.is_valid(): 
      orderform = form.save(commit=False)
      orderform.save()
      messages.info(request, 'Order Updated successfully!')
      return redirect('work:order_detail', order.id)
  context = {
      'page' : 'dashboard',
    'page_title' : 'Workshop - Dashoard',
    'order': order,
      'form': form,
  }

  return render(request,'workshop/order_management.html',context)


@login_required
def delete_order(request, order):
  try:
    sub = get_object_or_404(CustomerOrders,id=order)
    sub.delete()
    messages.success(request, 'Order deleted successfully')
    return redirect('work:paid_completed')
  except:
    messages.warning(request, 'Hmm..., the order not found!.')
    return redirect('work:paid_completed')




@login_required
def order_detail(request, order):
  order = CustomerOrders.objects.get(id=order)
  details = CustomerOrderDetail.objects.filter(order_id=order)
  form = OrderDetailForm()
  if request.method == "POST":
    form = OrderDetailForm(request.POST)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.order_id = order
      detailform.save()
      messages.success(request, 'item added successfully!')
      return redirect('work:order_detail', order.id)
  context = {
      'page' : 'dashboard',
    'page_title' : 'Order Details',
    'order': order,
    'form': form,
    'details': details
  }

  return render(request,'workshop/order_details.html',context)


@login_required
def updateItem(request, order, item):
  order = CustomerOrders.objects.get(id=order)
  details = CustomerOrderDetail.objects.filter(order_id=order)
  item = get_object_or_404(CustomerOrderDetail, id=item)

  form = OrderDetailForm(instance=item)
  if request.method == "POST":
    form = OrderDetailForm(request.POST, instance=item)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.order_id = order
      detailform.save()
      messages.success(request, 'item updated successfully!')
      return redirect('work:order_detail', order.id)
  context = {
    'page' : 'orders',
    'main_page' : 'orders',
    'page_title' : 'Order Details',
    'order': order,
    'form': form,
    'details': details,
    'item': item
  }

  return render(request,'workshop/order_details.html',context)    



@login_required
def inReviewOrderView(request):
  context = {
      'page' : 'in_review',
      'main_page' : 'orders',
      'page_title'  : 'In Review Order',
      'orders': CustomerOrders.objects.filter(work_status='New Job').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='New Job').count(),

  }
  return render(request,'workshop/orders.html',context)


@login_required
def activeOrderView(request):
  context = {
      'page' : 'active_work',
      'main_page' : 'orders',
      'page_title'  : 'Active Works',
      'orders': CustomerOrders.objects.filter(work_status='In Process').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='In Process').count(),

  }

  return render(request,'workshop/orders.html',context)



@login_required
def paidCompleted(request):
  context = {
      'page' : 'paid_completed',
      'main_page' : 'orders',
      'page_title'  : 'Job Paid Completed',
      'orders': CustomerOrders.objects.filter(work_status='Job paid completed').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='Job paid completed').count(),

  }

  return render(request,'workshop/orders.html',context)


@login_required
def canceledOrderView(request):
  context = {
      'page' : 'canceled_work',
      'main_page' : 'orders',
      'page_title'  : 'Canceled Works',
      'orders': CustomerOrders.objects.filter(work_status='Canceled').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='Canceled').count(),

  }

  return render(request,'workshop/orders.html',context)



@login_required
def jobCompletedNotPaid(request):
  context = {
      'page' : 'new_order',
      'main_page' : 'orders',
      'page_title'  : 'Job Completed Not Paid',
      'orders': CustomerOrders.objects.filter(work_status='Job completed not paid').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='Job completed not paid').count(),

  }

  return render(request,'workshop/orders.html',context)



@login_required
def jobCompletedNotPaid(request):
  context = {
      'page' : 'new_order',
      'main_page' : 'orders',
      'page_title'  : 'Job Completed Not Paid',
      'orders': CustomerOrders.objects.filter(work_status='Job completed not paid').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='Job completed not paid').count(),

  }

  return render(request,'workshop/orders.html',context)


@login_required
def jobPaidNotCompleted(request):
  context = {
      'page' : 'new_order',
      'main_page' : 'orders',
      'page_title'  : 'Job Completed Not Paid',
      'orders': CustomerOrders.objects.filter(work_status='Job paid not completed').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(work_status='Job paid not completed').count(),

  }

  return render(request,'workshop/orders.html',context)



@login_required
def paidInvoicesView(request):
  context = {
      'page' : 'paid',
      'main_page' : 'invoices',
      'page_title'  : 'Paid  Invoices',
      'orders': CustomerOrders.objects.filter(payment_status='Paid').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(payment_status='Paid').count(),

  }

  return render(request,'workshop/invoices.html',context)




@login_required
def unpaidInvoicesView(request):
  context = {
      'page' : 'unpaid',
      'main_page' : 'invoices',
      'page_title'  : 'Unpaid  Invoices',
      'orders': CustomerOrders.objects.filter(payment_status='Unpaid').order_by('-arrival_date'),
      'all_in_no' : CustomerOrders.objects.filter(payment_status='Unpaid').count(),

  }

  return render(request,'workshop/invoices.html',context)


@login_required
def previewInvoice(request, inv):
  order  = get_object_or_404(CustomerOrders, id=inv)
  context = {
      'page' : 'invoices',
      'main_page' : 'invoices',
      'page_title'  : 'preview invoice inv-'+str(order.id),
      'order': order,

  }
  return render(request,'workshop/invoice_preview.html',context)
  
@login_required
def invoicePrint(request, inv):
  order  = get_object_or_404(CustomerOrders, id=inv)
  context = {
      'page' : 'invoices',
      'main_page' : 'invoices',
      'page_title'  : 'preview invoice inv-'+str(order.id),
      'order': order,

  }
  return render(request,'workshop/printable_invoice.html',context)



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
      return redirect('work:add_vendor')
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Manage Vendor',
    'form': form,
    'vendors': vendors
  }

  return render(request,'workshop/manage_vendor.html',context)  


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
      return redirect('work:add_vendor')
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Manage Vendor',
    'form': form,
    'vendors': vendors
  }

  return render(request,'workshop/manage_vendor.html',context)  





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
      messages.success(request,'Order created successfully, sent to backoffice!')
      return redirect('work:inv_detail',invform.id )
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Invoice to '+vendor.vendor_name,
    'form': form,
    'vendor': vendor
  }

  return render(request,'workshop/vendor_invoices.html',context)  


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
      return redirect('work:inv_detail',invform.id )
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Invoice to '+vendor.vendor_name,
    'form': form,
    'vendor': vendor,
    'order' : order
  }

  return render(request,'workshop/vendor_invoices.html',context)  





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
      return redirect('work:inv_detail', order.id)
  context = {
    'page' : 'vendors',
    'main_page' : 'vendors',
    'page_title' : 'Order Details',
    'order': order,
    'form': form,
    'details': details
  }

  return render(request,'workshop/vendor_invoice_detail.html',context)    


@login_required
def requestInvoicesView(request):
  context = {
      'page' : 'requests',
      'main_page' : 'vendors',
      'page_title'  : 'All Requests ',
      'orders': VendorOrders.objects.all().order_by('-id'),
      'all_in_no' : VendorOrders.objects.all().count(),

  }
  return render(request,'workshop/all_requests.html',context)    


@login_required
def requestPreview(request, inv):
  order  = get_object_or_404(VendorOrders, id=inv)
  context = {
      'page' : 'requests',
      'main_page' : 'vendors',
      'page_title'  : 'preview request inv-'+str(order.id),
      'order': order,

  }
  return render(request,'workshop/request_preview.html',context)


@login_required
def printRequest(request, inv):
  order  = get_object_or_404(VendorOrders, id=inv)
  context = {
      'page' : 'requests',
      'main_page' : 'vendors',
      'page_title'  : 'Print Request -'+str(order.id),
      'order': order,

  }
  return render(request,'workshop/printable_request.html',context)



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
      return redirect('work:inv_detail', order.id)
  context = {
    'page' : 'requests',
    'main_page' : 'vendors',
    'page_title' : 'Order Details',
    'order': order,
    'form': form,
    'details': details,
    'item': item
  }

  return render(request,'workshop/vendor_invoice_detail.html',context)    



@login_required
def vendorComment(request, order):
  order = get_object_or_404(VendorOrders, id=order)
  if request.method == 'POST':
    comment = request.POST.get('comment','')
    newcomment = VendorOrderComment(order=order, staff=request.user, comment=comment) 
    newcomment.save()
    messages.success(request, 'Comment sent!')
    return redirect('work:inv_detail', order.id)
  else:
     messages.info(request, 'Comment not sent!')
     return redirect('work:inv_detail', order.id)
 




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
  

    return redirect('work:my_profile')
  context = {
    'page' : 'profile',
    'page_title' : str(request.user.username)+'\' profile',
   
    
  }
  return render(request,'workshop/my_profile.html',context)



@login_required
def addRequisition(request):
  form = RequisitionForm()
  requisitions = Requisition.objects.filter(request_by=request.user).order_by('-created_at')
  if request.method == "POST":
    form = RequisitionForm(request.POST)
    if form.is_valid(): 
     form = form.save(commit=False)
     form.request_by = request.user
     form.save()
     messages.success(request, 'Requisition added successfully!')
     return redirect('work:new_requisition')
  context = {
    'page' : 'manage_requisition',
    'main_page' : 'requisitions',
    'page_title' : 'Manage Requisition',
    'form': form,
    'requisitions': requisitions
  }

  return render(request,'workshop/manage_requisition.html',context)  

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
     return redirect('work:update_requisition', req.id)
  context = {
    'page' : 'manage_requisition',
    'main_page' : 'requisitions',
    'page_title' : 'Update Requisition',
    'form': form,
    'requisitions': requisitions
  }

  return render(request,'workshop/manage_requisition.html',context)  

@login_required
def requisitionDetails(request, requisition):
  order = Requisition.objects.get(id=requisition)
  details = RequisitionDetails.objects.filter(requisition=order)
  form = RequisitionDetailsForm()
  if request.method == "POST":
    form = RequisitionDetailsForm(request.POST)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.requisition = order
      detailform.save()
      messages.success(request, 'item added successfully!')
      return redirect('work:requisition_details', order.id)
  context = {
    'page' : 'manage_requisition',
    'main_page' : 'requisitions',
    'page_title' : 'Requisition Details',
    'order': order,
    'form': form,
    'details': details
  }

  return render(request,'workshop/requisition_details.html',context)    


@login_required
def updateRequisitionItem(request, requisition, desc):
  order = Requisition.objects.get(id=requisition)
  desc = get_object_or_404(RequisitionDetails, id=desc, requisition=order)
  details = RequisitionDetails.objects.filter(requisition=order)
  form = RequisitionDetailsForm(instance=desc)
  if request.method == "POST":
    form = RequisitionDetailsForm(request.POST, instance=desc)
    if form.is_valid(): 
      detailform = form.save(commit=False)
      detailform.requisition = order
      detailform.save()
      messages.success(request, 'item updated successfully!')
      return redirect('work:reqsupdate_item', order.id, desc.id)
  context = {
    'page' : 'manage_requisition',
    'main_page' : 'requisitions',
    'page_title' : 'Requisition Details',
    'order': order,
    'form': form,
    'details': details
  }

  return render(request,'workshop/requisition_details.html',context)    



@login_required
def requisitionPrint(request, req):
  order  = get_object_or_404(Requisition, id=req)
  context = {
      'page' : 'Requisition',
      'main_page' : 'Requisition',
      'page_title'  : 'preview requisition inv-'+str(order.id),
      'order': order,

  }
  return render(request,'workshop/printable_requisition.html',context)


@login_required
def allRequisition(request):
  requisitions = Requisition.objects.filter(request_by=request.user)
  context = {
    'page' : 'manage_requisition',
    'main_page' : 'requisitions',
    'page_title' : 'My Requisitions',
    'requisitions': requisitions
  }
  return render(request,'workshop/requisitions.html',context)


  #  job card no 
@login_required
def previewJobcard(request, inv):
  order  = get_object_or_404(CustomerOrders, id=inv)
  context = {
      'page' : 'Job Card Priview',
      'main_page' : 'jobs',
      'page_title'  : 'preview Job Card  J-'+str(order.id),
      'order': order,

  }
  return render(request,'workshop/job_card_preview.html',context)


@login_required
def cardPrint(request, inv):
  order  = get_object_or_404(CustomerOrders, id=inv)
  context = {
      'page' : 'Print',
      'main_page' : 'job',
      'page_title'  : 'preview Card inv-'+str(order.id),
      'order': order,

  }
  return render(request,'workshop/printable_card.html',context)


# #################### REPORTS ##################################

def generalReport(request):
  orders = None
  from_date = None
  to_date = None
  if request.method == 'POST':
    from_date = request.POST.get('from_date','')
    to_date = request.POST.get('to_date','')
    
    if from_date and to_date:
      fdate = datetime.strptime(from_date, "%Y-%m-%d")
      tdate = datetime.strptime(to_date, "%Y-%m-%d")
      orders  = CustomerOrders.objects.filter(departure_date__gte=fdate,departure_date__lte=tdate)
  
  context = {
    'page' : 'reports',
    'page_title' : 'General Report',
    'from_date':from_date,
    'to_date' : to_date,
    'orders': orders,



  }
  return render(request, 'workshop/report.html', context)
# #################### END REPORTS ##################################