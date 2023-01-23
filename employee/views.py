from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from datetime import timedelta
from django.contrib import messages
#models
from base.models import userInfo
from .models import employee_info
from appointment.models import appointment_available_dates, appointment_service
#forms
from .forms import employeeInfo

#user passes test for def not class
def manager_role_check(user):
    return user.role == userInfo.MANAGER

# Create your views here.
@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def employeeSearch(request):
    if request.method == 'POST':
        try:
            phone = request.POST['phone']            
            if phone:
                u = userInfo.objects.filter(phone=phone).get()
                if u.employee_info:
                    #pre fill employee info into form
                    data = {
                        "sg_address" : u.employee_info.sg_address,
                        "my_address" : u.employee_info.my_address,
                        "wp_id" : u.employee_info.wp_id,
                        "inner_role" : u.employee_info.inner_role,
                    }
                    eform = employeeInfo(initial=data)
                    #schedule date 
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
                    reuslt = appointment_available_dates.objects.filter(avail_date__range=[start_date, end_date], employee=u).all()
                    #input the dates into resultAvailDates using for loop
                    for r in reuslt:
                        resultAvailDates.append(r.avail_date)

                    context = {
                        "currentUser" : u,
                        "form" : eform,
                        "resultAvailDates" : resultAvailDates,
                        "list_dates" : list_dates
                    }
                    messages.success(request, f'Record found.')
                    return render(request, 'employee/employeeSearch.html', context=context) 
        except:
            messages.success(request, f'Error in finding record.')
            return render(request, 'employee/employeeSearch.html') 
    else:
        return render(request, 'employee/employeeSearch.html') 

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def employeeInfoSave(request):
    if request.method == 'POST':
        #find user employee
        u = userInfo.objects.get(pk=request.POST['employeeid'])
        eform = employeeInfo(request.POST)
        if eform.is_valid():
            #save mannually
            u.employee_info.sg_address = eform.cleaned_data['sg_address']
            u.employee_info.my_address = eform.cleaned_data['my_address']
            u.employee_info.wp_id = eform.cleaned_data['wp_id']
            u.employee_info.inner_role = eform.cleaned_data['inner_role']
            u.employee_info.save()
            messages.success(request, f'Employee record saved.')
            return redirect('employee-search')
        else:
            messages.warning(request, f'Error in saving employee record.')
            return redirect('employee-search')