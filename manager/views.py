from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
import datetime
from decimal import Decimal

#models
from notification.models import notification, ack_notification
from base.models import userInfo, contact
from .models import services, news, testimonial_pic
from appointment.models import appointment, appointment_service
from pos.models import sales_services, sales_transaction


#forms
from notification.forms import sendNotification
from base.forms import UpdateAccountInfo, UpdateProfilePic
from django.contrib import messages
from .forms import serviceform, newform, testimonialPic


from .forms import userCreationFormA, userSuspend

#user passes test for def not class
def manager_role_check(user):
    return user.role == userInfo.MANAGER

# Create your views here.

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def managerIndex(request):
    #get only upcoming appointments
    upcominga = appointment.objects.filter(status=1).all().order_by("-created_at")[0:9]
    upcomingcount = appointment.objects.filter(status=1).all().order_by("-created_at")
    #get sales 
    todaySales = sales_transaction.objects.filter(created_at__icontains=datetime.date.today()).all()
    latestSales = sales_transaction.objects.filter(created_at__icontains=datetime.date.today()).all().order_by("-created_at")[0:6]

    #upcoming display follow html table sequence
    upcomingTable = list()
    if upcominga:
        for ua in upcominga:
            templist = list()
            templist.append(ua.id)
            tempUsername = ua.user.first_name + " " + ua.user.last_name
            templist.append(tempUsername)
            tempEmployeeName = ua.employee.user.first_name + " " + ua.employee.user.last_name
            templist.append(tempEmployeeName)
            #get service
            resultService = ua.appointment_service_set.all()
            resultService = resultService[0].service.all()
            templist.append(resultService[0].service_name)
            templist.append(str(ua.appt_date.strftime("%Y-%m-%d / %H:%M")))
            templist.append("Upcoming")
            upcomingTable.append(templist)

    #calculate the total sales for today
    totalCurrentSales = 0.00
    if todaySales:
        for ts in todaySales:
            totalCurrentSales += float(ts.grand_total)

    context ={
        "upcomingTable" : upcomingTable,
        "upcomingcount" : upcomingcount,
        "totalCurrentSales" : totalCurrentSales,
        "latestSales" : latestSales,
    }
    return render(request, 'manager/mindex.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def userOverview(request):
    if request.method == "POST":
        try:
            user = userInfo.objects.get(email=request.POST["Email"])
            if not user.is_suspend:
                user.is_suspend = 1
                user.save()
                messages.success(request, f'User suspended')
            else:
                user.is_suspend = 0
                user.save()
                messages.success(request, f'User un-suspended')
            return redirect('manager-userOverview')
        except:
            messages.danger(request, f'Error in updating user')
            return redirect('manager-userOverview')

    allUsers = userInfo.objects.all().order_by("-date_joined")
    activeUsers = userInfo.objects.filter(is_active=1, is_suspend=0).all()
    suspendedUsers = userInfo.objects.filter(is_suspend=1).all()
    unverifiedEmailUsers = userInfo.objects.filter(is_active=0).all()

    #paginator
    paginator = Paginator(allUsers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    #context 
    context = {
        "activeUsers" : activeUsers.count(),
        "suspendedUsers" : suspendedUsers.count(),
        "unverifiedEmailUsers" : unverifiedEmailUsers.count(),
        "totalUsers" : allUsers.count(),
        "users" : page_obj,
        "userSuspendForm" : userSuspend,
    }

    return render(request, 'manager/userOverview.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def userCreate(request):
    if request.method == "POST":
        try:
            form = userCreationFormA(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'User created.')
                return redirect('manager-userOverview')
            else:
                messages.warning(request, f'Error in creating user, please try again.')
                return redirect('manager-userOverview')
        except:
            messages.warning(request, f'Error in creating user, please try again.')
            return redirect('manager-userOverview')
    else:
        context = {
            "form" : userCreationFormA(),
            
        }
    return render(request, 'manager/userCreate.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def userSearch(request):
    if request.method == "POST":
        try:
            searchUser = userInfo.objects.get(phone=request.POST["phone"])
            if searchUser:                
                data = {
                    'email' : searchUser.email,
                    'first_name' : searchUser.first_name,
                    'last_name' : searchUser.last_name,
                    'phone': searchUser.phone,
                    'dob' : searchUser.dob,                    
                }
               
                UpdateProfilePicForm = UpdateProfilePic()
                UpdateAccountInfoForm = UpdateAccountInfo(initial=data)	
                sendNotificationForm = sendNotification()
                
                #get all upcoming appointments for the user
                upcomingapp = ""
                upcomingapp = appointment.objects.filter(user=searchUser, status="UPCOMING").all().order_by("-created_at")
                context = {
                    "UpdateProfilePicForm" : UpdateProfilePicForm,
                    "UpdateAccountInfoForm" : UpdateAccountInfoForm,
                    "searchUser" : searchUser,
                    "sendNotificationForm" : sendNotificationForm,
                    'vouchers' : searchUser.voucher_set.all(),
                    "upcomingapp" : upcomingapp,
                }
                messages.success(request, f'User found.')
                return render(request, 'manager/userSearch.html', context=context)
        except:
            messages.warning(request, f'No user found.')
            redirect('manager-userSearch')

    return render(request, 'manager/userSearch.html')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def userSearchUpdate(request):
    try:
        if request.method == "POST":
            phonen = request.POST['phonen']
            ui = userInfo.objects.filter(phone=phonen).get()

            UpdateProfilePicForm = UpdateProfilePic(request.POST, request.FILES, instance=ui.profile_pic)
            UpdateAccountInfoForm = UpdateAccountInfo(request.POST, instance=ui)    

            if UpdateProfilePicForm.is_valid() and 	UpdateAccountInfoForm.is_valid():  
                UpdateProfilePicForm.save()                
                UpdateAccountInfoForm.save()
                messages.success(request, f'Your information has been updated.')
                return redirect("manager-userSearch")
    except:
        messages.warning(request, f'Eror in updating user profile. Please try again.')
        return redirect('manager-userOverview')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def userSuspendToogle(request):
    if request.method == "POST":
        try:
            u = userInfo.objects.get(email=request.POST['email'])
            if not u.is_suspend:
                u.is_suspend = 1
                u.save()
                messages.success(request, f'User status updated.')
                redirect('manager-userOverview')
            else:
                u.is_suspend = 0
                u.save()
                messages.success(request, f'User status updated.')
                redirect('manager-userOverview')
        except:
            messages.warning(request, f'Fail to update user status.')
            redirect('manager-userOverview')
    return redirect('manager-userOverview')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def userSendNotification(request):  
    try:  
        if request.method == "POST":
            sendNotificationForm = sendNotification(request.POST)
            if sendNotificationForm.is_valid():
                try:
                    u = userInfo.objects.get(email=request.POST['email'])                
                    if u:                    
                        sendNotificationForm.save()                    
                        ack_notification.objects.create(sent_user=u, sent_notification=sendNotificationForm.instance)
                        #send email to notify user
                        instanceNotification = sendNotificationForm.instance
                        send_mail(subject=instanceNotification.notification_title, message=instanceNotification.notification_description, from_email=settings.EMAIL_HOST_USER, recipient_list=[u.email])
                        
                        messages.success(request, f'Notification sent to user.')
                        return redirect('manager-userOverview')
                except:
                    messages.warning(request, f'Unable to send user notification.')
                    return redirect('manager-userOverview')
        
    except:
        messages.warning(request, f'Unable to send user notification.')
        return redirect('manager-userOverview')


@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def serviceOverview(request):
    if request.method == 'POST':
        try:
            serviceid = request.POST['serviceid']
            ss = services.objects.get(pk=serviceid)
            if ss:
                ss.delete()
                messages.success(request, f'Service deleted successfully.')
                return redirect('manager-serviceOverview')
            else:
                messages.warning(request, f'Service not available for delete.')
                return redirect('manager-serviceOverview')
        except:
            messages.warning(request, f'Error in deleting service.')
            return redirect('manager-serviceOverview')
    else:
        #request all services
        alls = services.objects.all().order_by("-created_at")

        #paginator
        paginator = Paginator(alls, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            "alls" : page_obj,
        }
        return render(request, 'manager/serviceOverview.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def serviceCreate(request):
    if request.method == 'POST':
        try:
            form = serviceform(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Service created: {form.cleaned_data["service_name"]}')
                return redirect('manager-serviceOverview')
        except:
            messages.success(request, f'Unable to create service. Please try again.')
            return redirect('manager-serviceOverview')
    else:
        form = serviceform()
        context = {
            "form" : form,
        }

        return render(request, 'manager/serviceCreate.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def serviceEdit(request):
    if request.method == 'POST':
        try:
            serviceInstance = services.objects.get(pk=request.POST['serviceid'])

            if serviceInstance: 
                form = serviceform(instance=serviceInstance)
                context = {
                    "form" : form,
                    "serviceid" : serviceInstance.id,
                }
                return render(request, 'manager/serviceEdit.html', context=context)
        except:
            messages.warning(request, f'Unable to edit service.')
            return redirect('manager-serviceOverview')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def serviceEditUpdate(request):
    if request.method == 'POST':
        try:
            serviceInstance = services.objects.get(pk=request.POST['serviceid'])
            form = serviceform(request.POST, instance=serviceInstance)
            if form.is_valid():
                form.save()
                messages.success(request, f'Service: [{serviceInstance.service_name}] updated. ')
                return redirect('manager-serviceOverview')
        except:
            messages.warning(request, f'Unable to update service. ')
            return redirect('manager-serviceOverview')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def contactOverview(request):
    try:
        if request.method == 'POST':
            #get var
            try:
                csid = request.POST['csid']
                cs = contact.objects.filter(pk=csid).get()
                if cs:
                    cs.is_ack = 1
                    cs.save()
                    messages.success(request, f'Contact id: {cs.id} acknowledged.')
                    return redirect("manager-contactOverview")
            except:
                messages.success(request, f'Unable to acknowledge contact.')
                return redirect("manager-contactOverview")
        else:
            contacts = contact.objects.filter(is_ack=0).all().order_by("-created_at")

            #paginator
            paginator = Paginator(contacts, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                "contacts" : page_obj,
            }
            return render(request, 'manager/contactOverview.html', context=context)
    except:
        contacts = contact.objects.filter(is_ack=0).all().order_by("-created_at")

        #paginator
        paginator = Paginator(contacts, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "contacts" : page_obj,
        }
        return render(request, 'manager/contactOverview.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def newsOverview(request):
    if request.method == 'POST':
        #get var
        try:
            newsInstance = news.objects.get(pk=request.POST['newsid'])
            if newsInstance:
                newsInstance.delete()
                messages.success(request, f'News deleted successfully.')
                return redirect('manager-newsOverview')
        except:
            messages.warning(request, f'Error in deleting news.')
            return redirect('manager-newsOverview')

    else:
        allNews = news.objects.all()
        print(allNews)
        #paginator
        paginator = Paginator(allNews, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            "allNews" : page_obj,
        }
        return render(request, 'manager/newsOverview.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def newsCreate(request):
    if request.method == 'POST':
        try:
            form = newform(request.POST)
            if form.is_valid():
                form.save()
                newstitle = form.cleaned_data['news_title']
                messages.success(request, f'News: {newstitle} saved successfully.')
                return redirect('manager-newsOverview')
            else:
                messages.success(request, f'Error in saving news.')
                return redirect('manager-newsOverview')
        except:
            messages.success(request, f'Error in saving news.')
            return redirect('manager-newsOverview')
    else:
        form = newform()
        context = {
            "form" : form
        }
        return render(request, 'manager/newsCreate.html', context=context)
    return render(request, 'manager/newsCreate.html')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def newsEdit(request):
    if request.method == 'POST':
        try:
            newsInstance = news.objects.get(pk=request.POST['newsid'])

            if newsInstance: 
                form = newform(instance=newsInstance)
                context = {
                    "form" : form,
                    "newsid" : newsInstance.id,
                }
                return render(request, 'manager/newsEdit.html', context=context)
        except:
            messages.warning(request, f'Unable to edit service.')
            return redirect('manager-newsOverview')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def newsEditUpdate(request):
    if request.method == 'POST':
        try:
            newsInstance = news.objects.get(pk=request.POST['newsid'])
            form = newform(request.POST, instance=newsInstance)
            if form.is_valid():
                form.save()
                messages.success(request, f'Service: [{newsInstance.news_title}] updated. ')
                return redirect('manager-newsOverview')
        except:
            messages.warning(request, f'Unable to update news. ')
            return redirect('manager-newsOverview')


@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def testimonialPicOverview(request):
    if request.method == 'POST':
        #get testid
        try:
            testid = request.POST['testid']
            testinstance = testimonial_pic.objects.get(pk=testid)
            if testinstance:
                testinstance.delete()
                messages.success(request, "Testimonla picture deleted.")
                return redirect('manager-testimonalOverview')
            else:
                messages.error(request, f'Error in deleting testimonal')
                return redirect('manager-testimonalOverview')
        except:
            messages.error(request, f'Error in deleting testimonal')
            return redirect('manager-testimonalOverview')
    else:
        #get all vars
        alltp = testimonial_pic.objects.all()

        context = {
            "alltp" : alltp,

        }
        return render(request, 'manager/testimonialOverview.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def createTestimonialPic(request):
    if request.method == 'POST':
        #get vars
        try:
            form = testimonialPic(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, f'Testimonal saved.')
                return redirect('manager-testimonalOverview')
            else:
                messages.error(request, f'Error in saving testimonal')
                return redirect('manager-testimonalOverview')
        except:
            messages.error(request, f'Error in saving testimonal')
            return redirect('manager-testimonalOverview')
    else:
        form = testimonialPic()
        context = {
            "form" : form,
        }

        return render(request, 'manager/createTestimonialPic.html', context=context)

