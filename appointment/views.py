from django.shortcuts import render, redirect
from verify_email.email_handler import send_verification_email
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import datetime

#import models
from .models import appointment_available_dates, appointment, appointment_service
from employee.models import employee_info
from manager.models import services
from base.models import userInfo


#time import
import datetime
from datetime import timedelta

#user passes test for def not class
def manager_role_check(user):
    return user.role == userInfo.MANAGER
def employee_role_check(user):
    return user.role == userInfo.EMPLOYEE
def employeeManager_role_check(user):
    if user.role == userInfo.EMPLOYEE or user.role == userInfo.MANAGER:
        return True

# Create your views here.

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def appointmentOverview(request):
    #get all appointments in 4 categories
    upcominga = appointment.objects.filter(status=1).all().order_by("-created_at")
    cancela = appointment.objects.filter(status=3).all().order_by("-created_at")
    misseda = appointment.objects.filter(status=5).all().order_by("-created_at")
    completeda = appointment.objects.filter(status=4).all().order_by("-created_at")
    #counter by html sequence
    countList = [upcominga.count(), cancela.count(), misseda.count(), completeda.count()]

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

    #cancel display follow html table sequence
    cancelTable = list()
    if cancela:
        for ua in cancela:
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
            templist.append("Cancel")
            cancelTable.append(templist)

    #missed display follow html table sequence
    missedTable = list()
    if misseda:
        for ua in misseda:
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
            templist.append("Missed")
            missedTable.append(templist)

    #upcoming display follow html table sequence
    completedTable = list()
    if completeda:
        for ua in completeda:
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
            templist.append("Completed")
            completedTable.append(templist)
    context = {
        "countList" : countList,
        "upcomingTable" : upcomingTable,
        "cancelTable" : cancelTable,
        "missedTable" : missedTable,
        "completedTable" : completedTable,
    }
    return render(request, 'appointment/appointmentOverview.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def appointmentSearch(request):
    try:
        if request.method == 'POST':
            #get vars
            customercphone = request.POST['searchcphone']
            c = userInfo.objects.filter(phone=customercphone).get()
            if c:
                apps = appointment.objects.filter(user=c).all()

                if apps:
                    #upcoming display follow html table sequence
                    completedTable = list()
                    if apps:
                        for ua in apps:
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
                            print(ua.status)
                            if ua.status == "1":
                                templist.append("Upcoming")
                            elif ua.status == "2":
                                templist.append("Cancel")
                            elif ua.status == "3":
                                templist.append("Cancel")
                            elif ua.status == "4":
                                templist.append("Completed")
                            elif ua.status == "5":
                                templist.append("Missed")
                            else:
                                templist.append("NIL")
                            completedTable.append(templist)
                    messages.success(request, f'{c.first_name} {c.last_name} appointments found')
                    return render(request, 'appointment/appointmentSearch.html', context={"completedTable":completedTable})
                else:
                    messages.warning(request, f'User exist but no appointment records found, please try again.')
                    return render(request, 'appointment/appointmentSearch.html')
            else:
                messages.warning(request, f'User does not exist, please try again.')
                return render(request, 'appointment/appointmentSearch.html')
    except:
        messages.warning(request, f'No appointment records found, please try again.')
        return render(request, 'appointment/appointmentSearch.html')

            
    return render(request, 'appointment/appointmentSearch.html')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def appointmentCreate(request):
    #get var
    employees = userInfo.objects.filter(role=2).all()
    customers = userInfo.objects.filter(role=1).all()
    context = {
        "employees" : employees,
        "customers" : customers,
    }
    return render(request, 'appointment/appointmentCreate.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def appointmentCalendar(reuqest):

    return render(reuqest, 'appointment/appointmentCal.html')

#Return appointments in JSON
#def all_appointments(request):

@login_required
@user_passes_test(employee_role_check, login_url='/login/')
def setAvailDate(request):
    #get two weeks in adv
    start_date = datetime.date.today()
    start_date2 = datetime.date.today()
    end_date = start_date + timedelta(weeks =3)
    delta = timedelta(days=1)
    list_dates = list()
    while start_date2 <= end_date:
        list_dates.append(start_date2)
        start_date2 += delta
    
    #query dates
    resultAvailDates = list()
    reuslt = appointment_available_dates.objects.filter(avail_date__range=[start_date, end_date], employee=request.user).all()
    #input the dates into resultAvailDates using for loop
    for r in reuslt:
        resultAvailDates.append(r.avail_date)
        
    context = {
        "subtitle" : "Schedule dates",
        "resultAvailDates" : resultAvailDates,
        "list_dates" : list_dates
    }
    return render(request, 'appointment/setDateSlot.html', context=context)

@login_required
@user_passes_test(employeeManager_role_check, login_url='/login/')
def toogleDatesEmployee(request):
    if request.method == "POST":
        date = request.POST['date']
        employee = request.POST['employee']
        employee = userInfo.objects.get(pk=employee)
        date = datetime.datetime.strptime(date, '%b. %d, %Y').date() 
        records = appointment_available_dates.objects.filter(avail_date=date, employee=employee).first()
        if not records:
            appointment_available_dates.objects.create(avail_date=date, employee=employee)
            success = 'Records: ' + str(date) + ' updated to NOT AVAILABLE.'
            return HttpResponse(success)
        else:
            appointment_available_dates.objects.filter(avail_date=date, employee=employee).delete()
            success = 'Records: ' + str(date) + ' updated to AVAILABLE.'
            return HttpResponse(success)
    else:
        success = 'Error in updating..'
        return HttpResponse(success)

@login_required
def userNewAppointment(request):
    employees = userInfo.objects.filter(role=2).all()
    context = {
        "subtitle" : "Book your appointment",
        "employees" : employees,
    }
    return render(request, 'appointment/userNewAppointment.html', context=context)

@login_required
def get_employee_dates(request):
    if request.method == 'POST':
        try:
            e = employee_info.objects.filter(user_id=request.POST['eid']).get()
            #get two weeks in adv
            start_date = datetime.date.today()
            start_date2 = datetime.date.today()
            end_date = start_date + timedelta(weeks =3)
            delta = timedelta(days=1)
            list_dates = list()
            while start_date2 <= end_date:
                list_dates.append(start_date2)
                start_date2 += delta
            
            #query dates
            resultAvailDates = list()
            resultAvailDates = appointment_available_dates.objects.filter(avail_date__range=[start_date, end_date], employee=e.pk).all()

            #String return 
            success = ""      
            #loop through and concat the output "success"  
            tempDates = list()  
            if resultAvailDates:        
                for rd in resultAvailDates:
                    tempDates.append(rd.avail_date)  

            if tempDates:
                for day in list_dates:
                    if day in tempDates:
                        pass                        
                    else:
                        success += "<option value='" + str(day) + "' onclick='etime()'>" + str(day) + "</option>" 
            else:                
                for day in list_dates:
                    temp = "<option value='" + str(day) + "' onclick='etime()'>" + str(day) + "</option>" 
                    success += temp 
                   
            return HttpResponse(success)
        except:
            success = "No result"
            return HttpResponse(success)


@login_required
def get_employee_time(request):
    if request.method == 'POST':
        try:
            edate = request.POST['edater']
            eid = request.POST['eid']            
            if eid and edate:
                time_list = list()
                success = ""
                result = appointment.objects.filter(appt_date__date=edate, employee=eid).exclude(status=3).all()
                #if result vaild then extract all the appt date HOURS                
                if result:
                    for r in result:
                        time_list.append(r.appt_date.strftime("%H"))
    
                output_list = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
                #Remove the time slot that was taken
                if time_list:
                    for tl in time_list:
                        if tl in output_list:
                            print(tl)
                            output_list.remove(tl)
                #construct the string output 
                for ol in output_list:
                    temp = "<option value='" + str(ol) + "' onclick='eservice()'>" + str(ol) + ":00 HRS</option>" 
                    success += temp
                return HttpResponse(success)
        except:
            success = "Error"
            return HttpResponse(success)


@login_required
def get_employee_service(request):
    if request.method == 'POST':
        try:     
            #get employee id       
            eid = request.POST['eid']
            employee = employee_info.objects.filter(user=eid).get()
            if employee:
                # get all services in the department
                service_list = list()
                if employee.inner_role == "both" or employee.inner_role == "BOTH":
                    service_list = services.objects.all()   
                else: 
                    service_list = services.objects.filter(department=employee.inner_role).all()                
                success = ""
                if service_list:
                    #construct the string output
                    for sl in service_list:
                        temp = "<option value='" + str(sl.id) + "' onclick='econfirm()'>" + str(sl.service_name) + "</option>" 
                        success += temp
                return HttpResponse(success)
        except:
            success = "Error"
            return HttpResponse(success)

@login_required
def get_econfirm(request):
    if request.method == 'POST':
        try:
            #get all attributes
            eid = request.POST['eid']
            edate = request.POST['edate']
            etime = request.POST['etime']
            eservice = request.POST['eservice']
            #retrive all instances 
            employee = employee_info.objects.filter(user=eid).get()
            service = services.objects.filter(pk=eservice).get()
            success = ""
            print(employee.user.first_name)
            if employee and service and edate and etime:
                tempEmployee = "<li class='list-group-item'>Cosmetology: " + employee.user.first_name + " " + employee.user.last_name + "</li>"
                tempDT = "<li class='list-group-item'>Date/Time: " + str(edate) + " / " + str(etime) + "00HRS</li>"
                tempService = "<li class='list-group-item'>Service: " + str(service.service_name) + "</li>"
                success += tempEmployee
                success += tempDT
                success += tempService
            return HttpResponse(success)
        except:
            success = "Error"
            return HttpResponse(success)

@login_required
def userBookAppointment(request):
    if request.method == 'POST':
        # get all values
        phoneORid = request.POST['currentUserId']
        if len(phoneORid) > 1:
            u = userInfo.objects.filter(phone=request.POST['currentUserId']).get()
        else:
            u = userInfo.objects.filter(pk=request.POST['currentUserId']).get()
        e = employee_info.objects.filter(user=request.POST['stylist']).get()
        datetime = str(request.POST['edater']) + " " + str(request.POST['etimer']) + ":00"
        svc = services.objects.filter(pk=request.POST['eservicer']).get()
        if u and e and datetime and svc:
            #create appointment first
            new_app = appointment.objects.create(appt_date=datetime, status=1, employee=e, user=u)
            if new_app:
                #create services linked to appointment
                app_svc_obj = appointment_service.objects.create()
                if app_svc_obj:
                    app_svc_obj.appointment.add(new_app)
                    app_svc_obj.service.add(svc)
                    messages.success(request, 'Your appointment has been created successfully.')
                    if request.user.role == 4:
                        return redirect('appointment-overview')
                    else:
                        return redirect('base-profile')

        messages.warning(request, 'Error in creating appointment, please try again.')
        if request.user.role == 4:
            return redirect('appointment-overview')
        else:
            return redirect('base-profile')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def changeAppointmentStatus(request):
    if request.method == 'POST':
        #get vars
        appid = request.POST['appid']
        statusupdate = request.POST['statusupdate']
        appt = appointment.objects.get(pk=appid)
        if appt and statusupdate:
            appt.status = statusupdate
            appt.save()
            messages.success(request, f'Status updated. AppointmentID: {appid}')
            return redirect('appointment-overview')
        else:
            messages.warning(request, f'Status update failed. AppointmentID: {appid}')
            return redirect('appointment-overview')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def searchCustomerPhone(request):
    if request.method == 'POST':
        try:
            customerphone = request.POST['customerphone']
            u = userInfo.object.filter(role=1, phone=customerphone).get()
            if u:
                success = "  "
                success += u.first_name + " " + u.last_name
                return HttpResponse(success)
        except:
            success = "invaild phone number"
            return HttpResponse(success)