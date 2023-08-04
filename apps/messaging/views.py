from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.messaging.models import Template


class TemplateListView(ListView):
    model = Template
    template_name = 'dashboard/template/template_list.html'
    context_object_name = 'templates'


class TemplateCreateView(CreateView):
    model = Template
    template_name = 'dashboard/template/template_form.html'
    fields = ['title', 'body', 'body_html', 'template_type', 're_usable', 'template_format', 'image_url', 'trigger_url']
    success_url = reverse_lazy('template_list')


class TemplateUpdateView(UpdateView):
    model = Template
    template_name = 'dashboard/template/template_form.html'
    fields = ['title', 'body', 'body_html', 'template_type', 're_usable', 'template_format', 'image_url', 'trigger_url']
    success_url = reverse_lazy('template_list')


class TemplateDeleteView(DeleteView):
    model = Template
    template_name = 'dashboard/template/template_confirm_delete.html'
    success_url = reverse_lazy('template_list')
