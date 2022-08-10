from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from Donation import models as m


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


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')


class FormView(View):
    def get(self, request):
        return render(request, 'form.html')


class FormConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')
