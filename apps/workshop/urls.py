from django.urls import path
from django.contrib.auth import views
from django.contrib.auth import views as auth_views #import this
from . import views

app_name = 'work'
urlpatterns = [
	path('',views.work_dashboard, name='dashboard'),
	path('customers/',views.customerView, name='customers'),
	path('customers/<int:customer>/update/',views.updateCustomer, name='update_customer'),
	path('invoice/',views.invoiceView, name='invoice'),
	path('order/<int:customer>/new-service/',views.newService, name='new_service'),
	path('order/<int:order>/management/',views.update_order, name='update_order'),
	path('order/<int:order>/order-detail/',views.order_detail, name='order_detail'),
	path('order/<int:order>/<int:item>/order-detail/',views.updateItem, name='update_item'),
	path('order/<int:order>/delete/',views.delete_order, name='delete_order'),
	path('order/<int:customer>/customer-orders/',views.ordersView, name='orders'),	
	path('orders/in-review/',views.inReviewOrderView, name='in_review'),
	path('orders/job-completed-not-paid/',views.jobCompletedNotPaid, name='completed_not_paid'),
	path('orders/job-paid-not-completed/',views.jobPaidNotCompleted, name='paid_not_completed'),
	path('orders/job-paid-completed/',views.paidCompleted, name='paid_completed'),
	path('orders/canceled-works/',views.canceledOrderView, name='canceled_work'),
	path('invoices/paid-invoices/',views.paidInvoicesView, name='paid_invoices'),
	path('invoices/unpaid-invoices/',views.unpaidInvoicesView, name='unpaid_invoices'),
	path('invoices/<int:inv>/preview/',views.previewInvoice, name='preview'),
	path('invoices/<int:inv>/print/',views.invoicePrint, name='invoice_print'),
	# vendor 
	path('vendor/add-new/',views.addVendor, name='add_vendor'),
	path('vendor/<int:vendor>/update/',views.updateVendor, name='update_vendor'),
	path('vendor/<int:vendor>/request/',views.vendorInvoice, name='vendor_invoice'),
	path('vendor/<int:vendor>/<int:order>/update-request/',views.UpdateVendorInvoice, name='update_request'),
	path('vendor/<int:order>/request-details/',views.vendor_invoice_detail, name='inv_detail'),
	path('vendor/<int:order>/order-comments/',views.vendorComment, name='vendor_comment'),
	path('vendor/all-requests/',views.requestInvoicesView, name='all_requests'),
	path('vendor/<int:inv>/request-preview/',views.requestPreview, name='request_preview'),
	path('vendor/<int:inv>/print-request/',views.printRequest, name='print_request'),
	path('vendor/<int:order>/<int:item>/request-detail/',views.updateVendorItem, name='update_vendor_item'),

	# 
	path('my-profile/',views.my_profile, name='my_profile'),

	# vendor 
	path('requisition/add-new/',views.addRequisition, name='new_requisition'),
	path('requisition/<int:requisition>/update/',views.updateRequisition, name='update_requisition'),
	path('requisition/<int:requisition>/details/',views.requisitionDetails, name='requisition_details'),
	path('requisition/<int:requisition>/<int:desc>/update-item/',views.updateRequisitionItem, name='reqsupdate_item'),
	path('requisition/<int:req>/requisition-pdf/',views.requisitionPrint, name='requisition_pdf'),
	path('requisition/my-requisitions/',views.allRequisition, name='my_requisitions'),

	# JOB CARD 
	path('job-card/<int:inv>/preview/',views.previewJobcard, name='card_preview'),
	path('job-card/<int:inv>/print/',views.cardPrint, name='card_print'),

	# REPORTS
	path('general/', views.generalReport, name='general_report')
	

	]

