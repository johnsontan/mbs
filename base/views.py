from django.shortcuts import render, redirect
from verify_email.email_handler import send_verification_email
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
import json

#forms
from .forms import MyUserCreationForm, LoginForm, UpdateAccountInfo, UpdateProfilePic, contactform, UpdateUserPassword

#models
from .models import userInfo
from notification.models import ack_notification, notification
from appointment.models import appointment, appointment_available_dates, appointment_service
from employee.models import employee_avail_leaves, employee_info, employee_leaves_history
from credit.models import credits, credits_history
from voucher.models import voucher, voucher_history
from manager.models import news
from manager.models import testimonial_pic

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

#EMAIL PASSWORD RESET IMPORT
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from .models import userInfo as User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.

def index(request):
	lastestNews = news.objects.all().order_by("-created_at")[0:4]
	latestTest = testimonial_pic.objects.all().order_by("-created_at")[0:6]
	context = {
		"lastestNews" : lastestNews,
		"latestTest" : latestTest,
	}
	return render(request, 'base/index.html', context=context)

def test(request):
	lastestNews = news.objects.all().order_by("-created_at")[0:4]
	context = {
		"lastestNews" : lastestNews,
	}
	return render(request, 'base/base.html', context=context)

def register_user(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            username_email = form.cleaned_data.get('email')
            messages.success(request, f'Account created, a verification link has been sent to your {username_email}.')
            return redirect('login')
    else:
        form = MyUserCreationForm()	
    return render(request, 'base/register.html', {'form': form, 'subtitle':'Register'})

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "base/password_reset_email.html"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Melon Beauty Salon',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'melonbeautysalonsg@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="base/password_reset.html", context={"password_reset_form":password_reset_form, "subtitle":"Reset password"})

def LoginView(request):
	if request.user.is_authenticated:
		return redirect('base-home')
	if request.method == "POST":
		subtitle = "Login"		
		form = LoginForm()		
		email = request.POST.get("email")
		password = request.POST.get("password")
		try: 
			user = userInfo.object.get(email=email)
			if user.check_password(password) and user.is_suspend == True:				
				messages.warning(request, f'Account suspended. Please contact the admin.')
				return render(request, 'base/login.html', {'form': form, 'subtitle' : subtitle})
			elif user.check_password(password) and user.is_active == False:
				messages.warning(request, f'A verification link sent to your {user.email}')
				return render(request, 'base/login.html', {'form': form, 'subtitle' : subtitle})
			elif user.check_password(password):				
				login(request, user)
				return redirect('base-profile')
			else:
				messages.warning(request, f'Email/Password incorrect.')
				return render(request, 'base/login.html', {'form': form, 'subtitle' : subtitle})
		except:
			messages.warning(request, f'Email/Password incorrect.')
			return render(request, 'base/login.html', {'form': form, 'subtitle' : subtitle})
	else:
		form = LoginForm()
		subtitle = "Login"
	
	return render(request, 'base/login.html', {'form': form, 'subtitle' : subtitle})

@login_required
def profile(request):
	#If POST
	if request.method == "POST":
		try:
			UpdateProfilePicForm = UpdateProfilePic(request.POST, request.FILES, instance=request.user.profile_pic)
			UpdateAccountInfoForm = UpdateAccountInfo(request.POST, instance=request.user)
			UpdateUserPasswordForm = UpdateUserPassword(request.POST)

			if UpdateProfilePicForm.is_valid() and 	UpdateAccountInfoForm.is_valid():
				UpdateAccountInfoForm.save()
				UpdateProfilePicForm.save()
				messages.success(request, f'Your information has been updated.')
				return redirect("base-profile")
			elif UpdateUserPasswordForm.is_valid():
				oldPassword = request.POST.get("oldPassword")
				pass1 = request.POST.get("password1")
				pass2 = request.POST.get("password2")
				user = userInfo.object.get(email=request.user.email)
				if user.check_password(oldPassword) and pass1 == pass2:
					user.set_password(pass1)
					user.save()
					messages.success(request, f'Password updated.')
					return redirect('base-profile')
				else:
					messages.warning(request, f'Password updated error.')
					return redirect('base-profile')
			else:
				messages.warning(request, f'Password updated error.')
				return redirect('base-profile')
		except:
			messages.warning(request, f'Please try again.')
			return redirect('base-profile')
	else:
	#retreive user information 
		user = userInfo.objects.filter(email=request.user.email).first()
		appcount = 0
		upcomingapps = list()
		apps = list()
		#get appointments based on roles (employee/customers)
		if user.role == 1:
			upcomingapps = appointment.objects.filter(user=user, status=1).all().order_by("-created_at")
			apps = appointment.objects.filter(user=user).exclude(status=1).all().order_by("-created_at")
		elif user.role == 2:
			upcomingapps = appointment.objects.filter(employee=user.id, status=1).all().order_by("-created_at")
			apps = appointment.objects.filter(employee=user.id).exclude(status=1).all().order_by("-created_at")
			
		if upcomingapps:
			appcount = upcomingapps.count()
		data = {
			'email' : user.email,
			'first_name' : user.first_name,
			'last_name' : user.last_name,
			'phone': user.phone,
			'dob' : user.dob,			
		}
		UpdateAccountInfoForm = UpdateAccountInfo(initial=data)	
		UpdateProfilePicForm = UpdateProfilePic()
		UpdateUserPasswordForm = UpdateUserPassword()

		#get user notifications
		userNotifications = ack_notification.objects.filter(sent_user=request.user, ack__isnull=True).all().order_by('-pk')

		#get credit history
		userCreditHistory = credits_history.objects.filter(user=request.user).all().order_by("-created_at")

		#get vouchers and voucher history
		userVouchers = voucher.objects.filter(user=request.user, qty__gt = 0).all()
		userVouchersHistory = voucher_history.objects.filter(user=request.user).all()

		context = {
			"subtitle" : "My profile",
			"UpdateAccountInfoForm" : UpdateAccountInfoForm,
			"UpdateProfilePicForm" : UpdateProfilePicForm,
			"UpdateUserPasswordForm" : UpdateUserPasswordForm,
			"userNotifications" : userNotifications,
			'appcount' : appcount,
			'upcomingapps' : upcomingapps,
			'apps' : apps,
			"userCreditHistory" : userCreditHistory,
			"userVouchers" : userVouchers,
			"userVouchersHistory" : userVouchersHistory,
		}
		return render(request, 'base/profile.html', context=context)

@login_required
def notification_ack(request):
	if request.method == "POST":
		try:
			ack_n = ack_notification.objects.get(pk=request.POST["notificationID"])
			if ack_n and ack_n.sent_user == request.user:
				ack_n.ack = timezone.now()
				ack_n.save()
				messages.success(request, f'Removed notification')
				return redirect("base-profile")
		except:
			messages.warning(request, f'error in removing notification')
			redirect("base-profile")
	else:
		return redirect("base-profile")

def serviceBeauty(request):
	context = {
		"subtitle": "Our beauty services"
	}
	return render(request, 'base/service_beauty.html', context=context)

def serviceHair(request):
	context = {
		"subtitle": "Our hair services"
	}
	return render(request, 'base/service_hair.html', context=context)


def aboutus(request):
	#get all employee info
	employees = userInfo.objects.filter(role=2).all()
	context = {
		"subtitle" : "About Us",
		"employees" : employees,
	}
	return render(request, 'base/aboutus.html', context=context)

def contact(request):
	if request.method == "POST":
		try:
			form = contactform(request.POST)
			if form.is_valid:
				form.save()
				messages.success(request, f'Your message has been sent, we will contact you in 3 business days.')
				return redirect('base-contact')
		except:
			messages.warning(request, f'An error has occurred, please try again.')
			return redirect('base-contact')
	else:
		form = contactform()

	context = {
		"form" : form,
		"subtitle" : "Contact us",
	}
	return render(request, 'base/contact.html', context=context)

@login_required
def moreAppInformation(request):
	if request.method == 'POST':
		#get vars
		aid = request.POST['aid']
		app = appointment.objects.get(pk=aid)
		if app:
			s = app.appointment_service_set.all()
			if s:
				success = ""
				success += "<p>Service: " + str(s[0].service.get().service_name) + "</p>"
				success += "<p>Cosmetology: " + app.employee.user.first_name + " " + app.employee.user.last_name + "</p>"
				success += "<p>Customer: " + app.user.first_name + " " + app.user.last_name + "</p>"
				success += "<p>Date/Time: " + app.appt_date.strftime("%d/%m/%Y / %H:%M") + "</p>"
				return HttpResponse(success)
	else:
		success = "Error"
		return HttpResponse(success)

def newsOverview(request):
	allNews = news.objects.all().order_by("-created_at")
	latestNews = news.objects.all().order_by("-created_at")[0:4]
	#paginator
	paginator = Paginator(allNews, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		"subtitle" : "News",
		"allNews" : page_obj,
		"latestNews" : latestNews,
	}
	return render(request, 'base/news.html', context=context)

def innerNews(request):
	if request.method == 'POST':
		try:
			newsid = request.POST['newsid']
			newsobj = news.objects.get(pk=newsid)
			if newsobj:
				context = {
					"newsobj" : newsobj,
					"subtitle": "News details"
				}
				return render(request, 'base/innerNews.html', context=context)
		except:
			messages.warning(request, f'Error in retrieving news.')
			return redirect('base-newsOverview')

def getNews(request):
	if request.method == 'POST':
		latestNews = news.objects.all().order_by("-created_at")[0:4]
		if latestNews:
			tempid = list()
			tempTitle = list()
			for ln in latestNews:
				#temp = "<li><form action='{%url 'base-innerNews'%}' method='post' id='news" + str(ln.id) + "'>{% csrf_token %}<input type='text' value='" + str(ln.id) + "'name='newsid' id='newsid' hidden readonly><a href='#' onclick='this.parentNode.submit(); return false;'>" + ln.news_title + "</a></form></li>"
				tempid.append(ln.id)
				tempTitle.append(ln.news_title) 
			success = list()
			success.append(tempid)
			success.append(tempTitle)
			return HttpResponse(json.dumps(success), content_type="application/json")
		else:
			success = "Error"
			return HttpResponse(success)

