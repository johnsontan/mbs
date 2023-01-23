from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from datetime import timedelta
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from decimal import Decimal

#models 
from .models import credits, credits_history
from base.models import userInfo

#user passes test for def not class

def manager_role_check(user):
    return user.role == userInfo.MANAGER

# Create your views here.
@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def creditOverview(request):
    #get all customer credits
    creditHistory = list()
    creditHistory = credits_history.objects.filter(created_at__contains=datetime.date.today()).all().order_by("-created_at")

    #paginator
    paginator = Paginator(creditHistory, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "creditHistory" : page_obj,
    }
        
    return render(request, 'credit/creditOverview.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def creditCD(request):
    return render(request, 'credit/creditCreditDeduct.html')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def creditSearch(request):
    if request.method == 'POST':
        #get vars
        try:
            phone = request.POST['cphone']
            u = userInfo.object.filter(phone=phone).get()
            creditHistory = list()
            creditHistory = credits_history.objects.filter(user=u).all().order_by("-created_at")
            if creditHistory:
                context = {
                    "creditHistory" : creditHistory,
                    "customer" : u,
                }
                messages.success(request, f'{u.first_name} {u.last_name} credit history found.')
                return render(request, 'credit/creditSearch.html', context=context)
            else:
                messages.warning(request, f'No records of credit history for {u.first_name} {u.last_name}.')
                return render(request, 'credit/creditSearch.html', context=context)
        except:
            messages.warning(request, f'Error in finding user.')
            return render(request, 'credit/creditSearch.html')
    else:
        return render(request, 'credit/creditSearch.html')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def debitCustomer(request):
    if request.method == 'POST':
        #get vars
        try:
            phone = request.POST['phone1']
            u = userInfo.objects.filter(phone=phone).get()
            uc = credits.objects.filter(user=u).get()
            amount = request.POST['amount1']
            transactionid = None
            transactionid = request.POST['transactionid1']
            remarks = request.POST['remarks1']
            type = "DEBIT"
            if u and uc:
                if transactionid:
                    credits_history.objects.create(user=u, amount=amount, type=type, transaction=transactionid, remarks=remarks)
                else:
                    credits_history.objects.create(user=u, amount=amount, type=type, remarks=remarks)
                uc.balance -= Decimal(amount)
                uc.save()
                messages.success(request, f'Debited customer[{u.first_name} {u.last_name}] account successfully.')
                return redirect("credit-overview")
            else:
                messages.warning(request, f'User/User credit record not found, please try agian.')
                return redirect("credit-overview")
        except:
            messages.warning(request, f'Error in debiting customer, please try agian.')
            return redirect("credit-overview")

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def creditCustomer(request):
    if request.method == 'POST':
        #get vars
        try:
            phone = request.POST['phone']
            u = userInfo.objects.filter(phone=phone).get()
            uc = credits.objects.filter(user=u).get()
            amount = request.POST['amount']
            transactionid = None
            transactionid = request.POST['transactionid']
            remarks = request.POST['remarks']
            type = "CREDIT"
            if u and uc:
                if transactionid:
                    credits_history.objects.create(user=u, amount=amount, type=type, transaction=transactionid, remarks=remarks)
                else:
                    credits_history.objects.create(user=u, amount=amount, type=type, remarks=remarks)
                uc.balance += Decimal(amount)
                uc.save()
                messages.success(request, f'Credited customer[{u.first_name} {u.last_name}] account successfully.')
                return redirect("credit-overview")
            else:
                messages.warning(request, f'User/User credit record not found, please try agian.')
                return redirect("credit-overview")
        except:
            messages.warning(request, f'Error in crediting customer, please try agian.')
            return redirect("credit-overview")

