from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class DashboardLoginView(TemplateView):
    template_name = "dashboard/accounts/login.html"


class DashboardIndexView(TemplateView):
    template_name = 'dashboard/index.html'


class DashboardEmptyView(TemplateView):
    template_name = 'dashboard/empty.html'
