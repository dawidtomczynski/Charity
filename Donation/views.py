import re
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from Donation import models as m


email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class BaseView(View):
    def get(self, request):
        bags_count = 0
        org_list = []
        donations = m.Donation.objects.all()
        for d in donations:
            bags_count += d.quantity
        for d in donations:
            if d.institution not in org_list:
                org_list.append(d.institution)
        org_count = len(org_list)
        funds = m.Institution.objects.filter(type=1)
        f_paginator = Paginator(funds, 5)
        f_page_number = request.GET.get('page')
        f_page_obj = f_paginator.get_page(f_page_number)
        orgs = m.Institution.objects.filter(type=2)
        o_paginator = Paginator(orgs, 5)
        o_page_number = request.GET.get('page')
        o_page_obj = o_paginator.get_page(o_page_number)
        locs = m.Institution.objects.filter(type=3)
        l_paginator = Paginator(locs, 5)
        l_page_number = request.GET.get('page')
        l_page_obj = l_paginator.get_page(l_page_number)
        return render(request, 'index.html', {'bags_count': bags_count, 'org_count': org_count,
                                              'funds': funds, 'orgs': orgs, 'locs': locs,
                                              'f_page_obj': f_page_obj, 'o_page_obj': o_page_obj,
                                              'l_page_obj': l_page_obj})


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if re.search(email_regex, email):
            if password1 == password2:
                User.objects.create_user(
                    first_name=name,
                    last_name=surname,
                    email=email,
                    username=email,
                    password=password1
                )
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('main')
        else:
            redirect('register')


class LogoutView(View):
    def get(self, request):
        if request.user:
            logout(request)
        return redirect('main')


class FormView(View):
    def get(self, request):
        return render(request, 'form.html')


class FormConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')
