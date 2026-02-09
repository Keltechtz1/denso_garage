from django.shortcuts import render, redirect,get_object_or_404

from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# change password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# other imports

from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.db.models import Sum



def login_view(request):
	valuenext = ''
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		valuenext= request.POST['next']
		user = auth.authenticate(username=username, password=password)

		if user is not None and valuenext=='':
		  auth.login(request, user)
		  messages.success(request, 'You have successfully logged in.')
		  if user.profile.role == 'Admin':
		    return redirect('office:dashboard')
		  elif  user.profile.role == 'Staff':
		  	 return redirect('work:dashboard')

		  return redirect('home')
		
		if user is not None and valuenext!='':
			auth.login(request, user)
			messages.success(request, "You have successfully logged in")
			return redirect(valuenext)
		else:
			messages.error(request, 'Invalid credentials')
			return redirect('home')
	return render(request, 'core/login.html')
