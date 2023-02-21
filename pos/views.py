from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
import json
from datetime import date
from django.http import HttpResponse
from decimal import Decimal

#models
from base.models import userInfo
from .models import sales_services, sales_transaction

#forms
from .forms import searchPosbyDate

#user passes test for def not class
def manager_role_check(user):
    return user.role == userInfo.MANAGER

# Create your views here.
@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def posStart(request):
    cash = sales_transaction.objects.filter(payment_type="CASH", created_at__contains=datetime.now().date()).all()
    credit = sales_transaction.objects.filter(payment_type="CREDIT", created_at__contains=datetime.now().date()).all()
    cards = sales_transaction.objects.filter(payment_type="CARDS", created_at__contains=datetime.now().date()).all()
    nets = sales_transaction.objects.filter(payment_type="NETS", created_at__contains=datetime.now().date()).all()
    grab = sales_transaction.objects.filter(payment_type="GRAB", created_at__contains=datetime.now().date()).all()
    paynow = sales_transaction.objects.filter(payment_type="PAYNOW", created_at__contains=datetime.now().date()).all()
    others = sales_transaction.objects.filter(payment_type="OTHERS", created_at__contains=datetime.now().date()).all()
    alltransaction = sales_transaction.objects.filter(created_at__contains=datetime.now().date()).all()
    employeeAll = userInfo.object.filter(role=2).all()

    #cal the total 
    cashT = 0.00
    creditT = 0.00
    cardsT = 0.00
    netsT = 0.00
    grabT = 0.00
    paynowT = 0.00
    othersT = 0.00

    if cash:
        for c in cash:
            cashT += float(c.grand_total)
    if credit:
        for c in credit:
            creditT += float(c.grand_total)
    if cards:
        for c in cards:
            cardsT += float(c.grand_total)
    if nets:
        for c in nets:
            netsT += float(c.grand_total)
    if grab:
        for c in grab:
            grabT += float(c.grand_total)
    if paynow:
        for pn in paynow:
            paynowT += float(pn.grand_total)
    if others:
        for c in others:
            othersT += float(c.grand_total)
    todaytotal = cashT + creditT + cardsT + netsT + grabT + othersT
    context = {
        "cash" : cashT,
        "credit" : creditT,
        "cards" : cardsT,
        "nets" : netsT,
        "grab" : grabT,
        "paynow" : paynowT,
        "others" : othersT,
        "todaytotal" : todaytotal,
        "employeeAll" : employeeAll,
        "alltransaction" : alltransaction,
    }

    return render(request, 'pos/startPOS.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def posEarnings(request):
    if request.method == 'GET':
        form = searchPosbyDate(request.GET)
        try:
            if form.is_valid() and form.cleaned_data['start_date'] <= datetime.now().date():
                endDate = form.cleaned_data['end_date']
                if endDate:                    
                    if endDate <= datetime.now().date():
                        if form.cleaned_data['employees'] is not None:                      
                            salesTransactions = sales_transaction.objects.filter(created_at__range=[form.cleaned_data['start_date'], endDate], employee=form.cleaned_data['employees'])                            
                        else:
                            salesTransactions = sales_transaction.objects.filter(created_at__range=[form.cleaned_data['start_date'], endDate])                            

                        #paginator
                        paginator = Paginator(salesTransactions, 20)
                        page_number = request.GET.get('page')
                        page_obj = paginator.get_page(page_number)

                        #Metrics 
                        grandTotal = float(0.00)
                        hairTotal = float(0.00)
                        service = float(0.00)
                        product = float(0.00)
                        beautyTotal = float(0.00)
                        creditTopup = float(0.00)
                        TransactionT = 0
                        paymentBreakdown = {
                            "cash" : float(0.00),
                            "credit" : float(0.00),
                            "cards" : float(0.00),
                            "nets" : float(0.00),
                            "grab" : float(0.00),
                            "paynow" : float(0.00),
                            "others" : float(0.00),
                        }

                        TransactionT = len(salesTransactions)
                        for st in salesTransactions:
                            grandTotal += float(st.grand_total)
                            if st.payment_type == "CASH":
                                paymentBreakdown['cash'] += float(st.grand_total)
                            elif st.payment_type == "CREDIT":
                                paymentBreakdown['credit'] += float(st.grand_total)
                            elif st.payment_type == "CARDS":
                                paymentBreakdown['cards'] += float(st.grand_total)
                            elif st.payment_type == "NETS":
                                paymentBreakdown['nets'] += float(st.grand_total)
                            elif st.payment_type == "GRAB":
                                paymentBreakdown['grab'] += float(st.grand_total)
                            elif st.payment_type == "PAYNOW":
                                paymentBreakdown["paynow"] += float(st.grand_total)
                            elif st.payment_type == "OTHERS":
                                paymentBreakdown['others'] += float(st.grand_total)
                            for ss in st.sales_services_set.all():
                                if ss.service_department == "HAIR":
                                    service += float(ss.service_price)
                                    hairTotal += float(ss.service_price)
                                elif ss.service_department == "HAIR PRODUCT":
                                    product += float(ss.service_price)
                                    hairTotal += float(ss.service_price)
                                elif ss.service_department == "BEAUTY":
                                    service += float(ss.service_price)
                                    beautyTotal += float(ss.service_price)
                                elif ss.service_department == "BEAUTY PRODUCT":
                                    product += float(ss.service_price)
                                    beautyTotal += float(ss.service_price)
                                elif ss.service_department == "CREDIT TOP UP":
                                    creditTopup += float(ss.service_price)
                        

                        context = {
                            "salesT" : page_obj,
                            "form" : form,
                            "start_date" : form.cleaned_data['start_date'],
                            "end_date" : endDate,
                            "employees" : form.cleaned_data['employees'],
                            "csrfToken" : request.GET.get('csrfmiddlewaretoken'),  
                            "grandTotal" : round(grandTotal, 2),
                            "hairTotal" : round(hairTotal, 2),
                            "beautyTotal" : round(beautyTotal, 2),
                            "TransactionT" : TransactionT,
                            "paymentBreakdown" : paymentBreakdown, 
                            "creditTopupT" : creditTopup, 
                            "serviceT" : round(service, 2),
                            "productT" : round(product, 2),                    
                        }

                        messages.success(request, f'Sales records found.')
                        return render(request, 'pos/posEarnings.html', context=context)
                    else:
                        #END DATE IS MORE THE CURRENT DATE
                        messages.warning(request, f'End date out of range. Please try again.')
                        return redirect('pos-earnings')
                else:
                    
                    if form.cleaned_data['employees'] is not None:
                        salesTransactions = sales_transaction.objects.filter(created_at__icontains=form.cleaned_data['start_date'], employee=form.cleaned_data['employees'])                        
                    else:
                        salesTransactions = sales_transaction.objects.filter(created_at__icontains=form.cleaned_data['start_date'])
                        

                    #paginator
                    paginator = Paginator(salesTransactions, 20)
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)

                    #Metrics 
                    grandTotal = float(0.00)
                    hairTotal = float(0.00)
                    beautyTotal = float(0.00)
                    service = float(0.00)
                    product = float(0.00)
                    creditTopup = float(0.00)
                    TransactionT = 0

                    paymentBreakdown = {
                        "cash" : float(0.00),
                        "credit" : float(0.00),
                        "cards" : float(0.00),
                        "nets" : float(0.00),
                        "grab" : float(0.00),
                        "paynow" : float(0.00),
                        "others" : float(0.00),
                    }
                    TransactionT = len(salesTransactions)
                    for st in salesTransactions:
                        grandTotal += float(st.grand_total)
                        if st.payment_type == "CASH":
                            paymentBreakdown['cash'] += float(st.grand_total)
                        elif st.payment_type == "CREDIT":
                            paymentBreakdown['credit'] += float(st.grand_total)
                        elif st.payment_type == "CARDS":
                            paymentBreakdown['cards'] += float(st.grand_total)
                        elif st.payment_type == "NETS":
                            paymentBreakdown['nets'] += float(st.grand_total)
                        elif st.payment_type == "GRAB":
                            paymentBreakdown['grab'] += float(st.grand_total)
                        elif st.payment_type == "PAYNOW":
                            paymentBreakdown['paynow'] += float(st.grand_total)
                        elif st.payment_type == "OTHERS":
                            paymentBreakdown['others'] += float(st.grand_total)
                        for ss in st.sales_services_set.all():
                            if ss.service_department == "HAIR":
                                service += float(ss.service_price)
                                hairTotal += float(ss.service_price)
                            elif ss.service_department == "HAIR PRODUCT":
                                product += float(ss.service_price)
                                hairTotal += float(ss.service_price)
                            elif ss.service_department == "BEAUTY":
                                service += float(ss.service_price)
                                beautyTotal += float(ss.service_price)
                            elif ss.service_department == "BEAUTY PRODUCT":
                                product += float(ss.service_price)
                                beautyTotal += float(ss.service_price)
                            elif ss.service_department == "CREDIT TOP UP":
                                    creditTopup += float(ss.service_price)
                    

                    context = {
                        "salesT" : page_obj,
                        "form" : form,
                        "start_date" : form.cleaned_data['start_date'],
                        "employees" : form.cleaned_data['employees'],
                        "csrfToken" : request.GET.get('csrfmiddlewaretoken'),
                        "grandTotal" : round(grandTotal,2),
                        "hairTotal" : round(hairTotal,2),
                        "beautyTotal" : round(beautyTotal,2),
                        "TransactionT" : round(TransactionT,2),
                        "creditTopupT" : creditTopup,
                        "paymentBreakdown" : paymentBreakdown,
                        "productT" : round(product,2),
                        "serviceT" : round(service,2),
                    }
                    messages.success(request, f'Sales records found.')
                    return render(request, 'pos/posEarnings.html', context=context)
                ###########
            else:
                form = searchPosbyDate()
                sd= ed= start_date= end_date = salesTransactions = ""

                sd = request.GET.get('start_date')
                ed = request.GET.get('end_date')

                if sd and ed:
                    start_date = datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y").date()
                    end_date = datetime.strptime(request.GET.get('end_date'), "%b. %d, %Y").date()
                elif sd:
                    start_date = datetime.strptime(request.GET.get('start_date'), "%b. %d, %Y").date()
                
                csrfToken = request.GET.get('csrfToken')

                if start_date and end_date:
                    if request.GET.get('employees') is not None:
                        salesTransactions = sales_transaction.objects.filter(created_at__range=[start_date, end_date], employee=request.GET.get('employees'))
                    else:
                        salesTransactions = sales_transaction.objects.filter(created_at__range=[start_date, end_date])
                elif start_date:
                    if request.GET.get('employees') is not None:
                        salesTransactions = sales_transaction.objects.filter(created_at__icontains=start_date, employee=request.GET.get('employees'))
                    else:
                        salesTransactions = sales_transaction.objects.filter(created_at__icontains=start_date)

                #paginator
                paginator = Paginator(salesTransactions, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)

                #Metrics 
                grandTotal = float(0.00)
                hairTotal = float(0.00)
                beautyTotal = float(0.00)
                service = float(0.00)
                product = float(0.00)
                creditTopup = float(0.00)
                TransactionT = 0
                                
                paymentBreakdown = {
                    "cash" : float(0.00),
                    "credit" : float(0.00),
                    "cards" : float(0.00),
                    "nets" : float(0.00),
                    "grab" : float(0.00),
                    "paynow" : float(0.00),
                    "others" : float(0.00),
                }
                TransactionT = len(salesTransactions)
                for st in salesTransactions:
                    grandTotal += float(st.grand_total)
                    if st.payment_type == "CASH":
                        paymentBreakdown['cash'] += float(st.grand_total)
                    elif st.payment_type == "CREDIT":
                        paymentBreakdown['credit'] += float(st.grand_total)
                    elif st.payment_type == "CARDS":
                        paymentBreakdown['cards'] += float(st.grand_total)
                    elif st.payment_type == "NETS":
                        paymentBreakdown['nets'] += float(st.grand_total)
                    elif st.payment_type == "GRAB":
                        paymentBreakdown['grab'] += float(st.grand_total)
                    elif st.payment_type == "PAYNOW":
                        paymentBreakdown['paynow'] += float(st.grand_total)
                    elif st.payment_type == "OTHERS":
                        paymentBreakdown['others'] += float(st.grand_total)
                    for ss in st.sales_services_set.all():
                        if ss.service_department == "HAIR":
                            service += float(ss.service_price)
                            hairTotal += float(ss.service_price)
                        elif ss.service_department == "HAIR PRODUCT":
                            product += float(ss.service_price)
                            hairTotal += float(ss.service_price)
                        elif ss.service_department == "BEAUTY":
                            service += float(ss.service_price)
                            beautyTotal += float(ss.service_price)
                        elif ss.service_department == "BEAUTY PRODUCT":
                            product += float(ss.service_price)
                            beautyTotal += float(ss.service_price)
                        elif ss.service_department == "CREDIT TOP UP":
                            creditTopup += float(ss.service_price)
            

                context = {
                    "form" : form,
                    "salesT" : page_obj,
                    "start_date" : start_date,
                    "end_date" : end_date,
                    "employees" : request.GET.get('employees'),
                    "csrfToken" : request.GET.get('csrfmiddlewaretoken'),
                    "grandTotal" : round(grandTotal,2),
                    "hairTotal" : round(hairTotal,2),
                    "beautyTotal" : round(beautyTotal,2),
                    "creditTopupT" : creditTopup,
                    "TransactionT" : TransactionT,
                    "paymentBreakdown" : paymentBreakdown,
                    "serviceT" : round(service,2),
                    "productT" : round(product,2),
                }
                return render(request, 'pos/posEarnings.html', context=context)
        except:
            messages.warning(request, f'Error in getting records. Please try again.')
            return redirect('pos-earnings')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def posReceipt(request):
    if request.method == 'POST':
        try:
            stall = sales_transaction.objects.get(pk=request.POST['salesid'])
            if stall:
                ssall = stall.sales_services_set.all()
                context = {
                    "stall" : stall,
                    "ssall" : ssall,
                    "subtotal" : round(stall.grand_total * Decimal(0.92), 2),
                    "gst" : round(stall.grand_total * Decimal(0.08),2),
                }
                return render(request, 'pos/posReceipt.html', context=context)
        except:
            messages.warning(request, f'Error in retrieving entry')
            return redirect('pos-receipt')
    else:
        return render(request, 'pos/posReceipt.html')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def posTransact(request):
    if request.method == 'POST':
        #get vars
        try:
            phone = request.POST['customerid']
            cs = ""
            if phone:
                cs = userInfo.objects.filter(phone=phone).get()
            employeeid = request.POST['employeeid']
            em = userInfo.objects.get(pk=employeeid)
            sn = request.POST.getlist('serviceName[]')
            sp = request.POST.getlist('servicePrice[]')
            sd = request.POST.getlist('serviceDepartment[]')
            grandtotal = request.POST['grandtotal']
            remarks = request.POST['remarks']
            ttype = request.POST['ttype']

            if len(sn) != len(sp) != len(sd):
                messages.warning(request, f'Error in services, please try again.')
                return redirect('pos-start')
            
            #service price == grand total
            tempPrice = 0.00
            for ssp in sp:
                tempPrice += round(float(ssp), 2)
            if tempPrice != round(float(grandtotal), 2):
                messages.warning(request, f'Service price do not match with Grand Total, please try again.')
                return redirect('post-start')

            if cs:
                st = sales_transaction.objects.create(payment_type=ttype, grand_total=grandtotal, employee=em, customer=cs, remarks=remarks)
            else:
                st = sales_transaction.objects.create(payment_type=ttype, grand_total=grandtotal, employee=em, remarks=remarks)
            if st:
                for idx, x in enumerate(sn):
                    sales_services.objects.create(service_name=x, service_price=sp[idx], sales_id=st, service_department=sd[idx])
                messages.success(request, f'Successfully transact')
                return redirect('pos-start')
        except:
            messages.warning(request, f'Error in recording transaction, please try again.')
            return redirect('pos-start')


@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def rservice(request):
    if request.method == 'POST':
        #get vars

        rsid = request.POST['rsid']
        st = sales_transaction.objects.get(pk=rsid)
        if st: 
            ss = sales_services.objects.filter(sales_id=st).all()
            if ss:
                success = ""
                for s in ss:
                    temp = "<p>Service: " + s.service_name + "</p><p>Price: " + str(s.service_price) + "</p><p>Department: " + s.service_department + "</p><p>Payment type: " + s.sales_id.payment_type + "</p><p>Remarks: " + s.sales_id.remarks + "</p><hr>"
                    success += temp
                return HttpResponse(success)
        else:
            success = "Error"
            return HttpResponse(success)