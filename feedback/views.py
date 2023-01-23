from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from base.models import userInfo

#user passes test for def not class
def manager_role_check(user):
    return user.role == userInfo.MANAGER

# Create your views here.

@login_required
@user_passes_test(manager_role_check, login_url='/login/')
def feedbackOverview(request):
    return render(request, 'feedback/feedbackOverview.html')