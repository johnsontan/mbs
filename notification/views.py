from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages

#models
from base.models import userInfo
from .models import notification, ack_notification

#forms
from .forms import sendNotification


#user passes test for def not class
def manager_role_check(user):    
    return user.role == userInfo.MANAGER

# Create your views here.
@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def notificationOverview(request):
    #get all notification
    allNotification = notification.objects.all().order_by("-created_at")
    #extract all notification with user email
    extractNotification = list()
    for an in allNotification:
        tempID = an.id
        tempSubject = an.notification_title
        tempDesc = an.notification_description
        tempList = list()
        for u in an.ack_notification_set.all():
            tempList.append(u.sent_user.email)
        tempDict = {"subject": tempSubject, "desc": tempDesc, "users":tempList, "id" :tempID,}
        extractNotification.append(tempDict)

    #paginator
    paginator = Paginator(extractNotification, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "allNotification" : page_obj,
        "notificationCount": allNotification.count(),
    }
    return render(request, 'notification/notificationOverview.html', context=context)


@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def notificationsend(request):
    if request.method == "POST":
        try:
            allUsers = userInfo.objects.filter(role=1).all()                     
            form = sendNotification(request.POST)           
            if form.is_valid():                
                form.save()
                for u in allUsers:
                    ack_notification.objects.create(sent_notification=form.instance, sent_user=u)
                messages.success(request, f'Notification sent to all users.')
                return redirect('notification-send')
        except:
            messages.warning(request, f'Fail to mass send notification.')
            return redirect('notification-send')
    else:
        form = sendNotification()
        context={
            "form" : form,
        }
    return render(request, 'notification/notificationSend.html', context=context)


@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def notificationSearch(request):
    if request.method == "POST":
        try:
            notificationT = request.POST['notificationTitle']
            if notificationT:
                resultNotification = notification.objects.filter(notification_title__icontains=notificationT).all()
                if resultNotification:
                    #extract all notification with user email
                    extractNotification = list()
                    for an in resultNotification:
                        tempID = an.id
                        tempSubject = an.notification_title
                        tempDesc = an.notification_description
                        tempList = list()
                        for u in an.ack_notification_set.all():
                            tempList.append(u.sent_user.email)
                        tempDict = {"subject": tempSubject, "desc": tempDesc, "users":tempList, "id" :tempID,}
                        extractNotification.append(tempDict)
                    context = {
                        "allNotification" : extractNotification,
                        "numberNotification": len(extractNotification),
                    }
                    messages.success(request, f'Notification records found.')
                    return render(request, 'notification/notificationSearch.html', context=context)
                else:
                    messages.warning(request, f'Error in finding notification records, please try again.')
                    return render(request, 'notification/notificationSearch.html')
        except:
            messages.warning(request, f'Error in finding notification records, please try again.')
            return render(request, 'notification/notificationSearch.html')

    else:
        return render(request, 'notification/notificationSearch.html')