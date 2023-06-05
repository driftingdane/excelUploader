from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from csv_upload.views import user_list

from .forms import RegisterForm, UserEditForm
from .models import NewUser
from .token import account_activation_token

# @login_required
# def edit_details(request):
# 	if request.method == 'POST':
# 		user_form = UserEditForm(instance=request.user, data=request.POST)
# 		if user_form.is_valid():
# 			user_form.save()
# 	else:
# 		user_form = UserEditForm(instance=request.user)
#
# 	return render(request, 'users/user/edit_details.html', {'user_form': user_form})
#
#
# @login_required
# def delete_user(request):
# 	user = NewUser.objects.get(user_name=request.user)
# 	user.is_active = False
# 	user.save()
# 	logout(request)
# 	return redirect('users:delete_confirmation')
#
# def register(request):
# 	if request.user.is_authenticated and not request.user.is_staff:
# 		return redirect('users:dashboard')
#
# 	if request.method == 'POST':
# 		regForm = RegisterForm(request.POST)
# 		if regForm.is_valid():
# 			user = regForm.save(commit=False)
# 			user.email = regForm.cleaned_data['email']
# 			user.set_password(regForm.cleaned_data['password'])
# 			user.is_active = False
# 			user.save()
# 			# Setup email
# 			current_site = get_current_site(request)
# 			subject = 'Activate your Account'
# 			message = render_to_string('users/register/activation_email.html', {
# 				'user': user,
# 				'domain': current_site.domain,
# 				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
# 				'token': account_activation_token.make_token(user),
# 			})
# 			user.email_user(subject=subject, message=message)
# 			# messages.success(request, 'Sign up successful and activation sent')
# 			# return render(request, "users/register/login.html")
# 			# messages.success(request, 'Sign up successful and activation sent')
# 			return HttpResponse(memoryview(b'Sign up successful and activation sent'))
# 	# return TemplateResponse(request, 'users/register/login.html')
# 	else:
# 		regForm = RegisterForm()
# 	return render(request, 'users/register/register.html', {'form': regForm})
#
#
# def account_activate(request, uidb64, token):
# 	try:
# 		uid = force_text(urlsafe_base64_decode(uidb64))
# 		user = NewUser.objects.get(pk=uid)
# 	except(TypeError, ValueError, OverflowError, user.DoesNotExist):
# 		user = None
# 	if user is not None and account_activation_token.check_token(user, token):
# 		user.is_active = True
# 		user.save()
# 		login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
# 		return redirect('users:login')
# 	else:
# 		return render(request, 'users/register/activation_invalid.html')
