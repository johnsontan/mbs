from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse

#import models
from base.models import userInfo
from .models import voucher, voucher_history

#import forms
from .forms import signForm

#user passes test for def not class
def manager_role_check(user):
    return user.role == userInfo.MANAGER

# Create your views here.
@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def voucherOverview(request):
    #get all voucher histroy 
    vh = voucher_history.objects.all().order_by("-created_at")

    #paginator
    paginator = Paginator(vh, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "voucherHistory" : page_obj,
    }

    return render(request, 'voucher/voucherOverview.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def voucherCredit(request):
    if request.method == 'POST':
        try:
            #get var
            phone = request.POST['cphone']
            u = userInfo.objects.filter(phone=phone).get()
            vouchername = request.POST['vouchername']
            qty = request.POST['voucherqty']
            grandtotal = request.POST['grandtotal']
            eachtime = request.POST['eachtime']
            if u and vouchername and qty and grandtotal and eachtime:
                vc = voucher.objects.create(voucher_name=vouchername, qty=qty, tqty=qty, user=u, grand_total=grandtotal, eachtime=eachtime)
                voucher_history.objects.create(user=u, voucher=vc, type="CREDIT", voucher_amount=qty)
                messages.success(request, f'Voucher [{vouchername}] issued to customer successfully.')
                return redirect('voucher-overview')
        except:
            messages.danger(request, f'[{vouchername}] unable to issue.')
            return redirect('voucher-overview')
    return render(request, 'voucher/voucherCredit.html')

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def voucherDebit(request):
    if request.method == 'POST':
        #get vars
        form = signForm(request.POST)
        phone = request.POST['cphone']
        u = userInfo.objects.filter(phone=phone).get()
        vid = request.POST['vouchername']
        qty = request.POST['voucherqty']
        vc = voucher.objects.get(pk=vid)
        if int(vc.qty) - int(qty) >= 0 and form.is_valid():
            vc.qty -= int(qty)
            vc.save()
            voucher_history.objects.create(user=u, voucher=vc, type="DEBIT", voucher_amount=qty, signature=form.cleaned_data['signature'])
            messages.success(request, f'Voucher [{vc.voucher_name}] deducted {qty} times. Balance: {vc.qty}')
            return redirect('voucher-overview')
        else:
            messages.warning(request, f'Voucher quantity error.')
            return redirect('voucher-debit')
    else:
        form = signForm()
        context = {
            "signForm" : form,
        }
        return render(request, 'voucher/voucherDebit.html', context=context)

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def voucherSearch(request):
    if request.method == 'POST':
        
        #get voucher title
        title = request.POST['searchTitle']
        voucherInstances = voucher.objects.filter(voucher_name__icontains=title).all()
        if voucherInstances:
            returnVList = list()
            for vi in voucherInstances:
                templist = list()
                #name
                templist.append(vi.voucher_name)
                tempName = str(vi.user.first_name) + str(vi.user.last_name)
                templist.append(tempName)
                templist.append(vi.user.phone)
                templist.append(vi.qty)
                templist.append(vi.tqty)
                templist.append(vi.grand_total)
                templist.append(vi.created_at.strftime("%d-%m-%Y"))
                tempHistory = list()
                viHistory = vi.voucher_history_set.all()
                if viHistory:
                    for vh in viHistory:
                        tempHistory.append(vh)
                    templist.append(tempHistory)
                    returnVList.append(templist)                    
                else:
                    returnVList.append(templist)
            messages.success(request, f'Vouchers records found')
            context = {
                "returnVList" : returnVList,
            }
            return render(request, 'voucher/voucherSearch.html', context=context) 
        else:
            messages.warning(request, f'No vouchers exists, please try again.')
            return render(request, 'voucher/voucherSearch.html')
    else:
        return render(request, 'voucher/voucherSearch.html')


@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def findCustomerVoucher(request):
    if request.method == 'POST':
        try:
            #get user
            phone = request.POST['customerphone']
            u = userInfo.objects.filter(phone=phone).get()
            if u:
                vouchers = voucher.objects.filter(user=u.id, qty__gt=0).all().order_by("-created_at")
                if vouchers:
                    success = ""
                    for vc  in vouchers:
                        temp = "<option value='" + str(vc.id) +"'>" + str(vc.voucher_name) + "</option>"
                        success += temp
                    return HttpResponse(success)
        except:
            success = "No vouchers found"
            return HttpResponse(success)        