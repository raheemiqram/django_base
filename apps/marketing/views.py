from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory

from .models import Audience, Rule


class AudienceListView(ListView):
    model = Audience
    template_name = 'dashboard/audience/audience_list.html'


class AudienceDetailView(DetailView):
    model = Audience
    template_name = 'dashboard/audience/audience_detail.html'


class AudienceCreateView(CreateView):
    model = Audience
    fields = ['name', 'description']
    template_name = 'dashboard/audience/audience_form.html'
    success_url = reverse_lazy('audience-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['rules'] = RuleInlineFormSet(self.request.POST)
        else:
            data['rules'] = RuleInlineFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        rules = context['rules']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if rules.is_valid():
                rules.instance = self.object
                rules.save()
        return super().form_valid(form)


class AudienceUpdateView(UpdateView):
    model = Audience
    fields = ['name', 'description']
    template_name = 'dashboard/audience/audience_form.html'
    success_url = reverse_lazy('audience-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['rules'] = RuleInlineFormSet(self.request.POST, instance=self.object)
        else:
            data['rules'] = RuleInlineFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        rules = context['rules']
        with transaction.atomic():
            form.instance.modified_by = self.request.user
            self.object = form.save()
            if rules.is_valid():
                rules.instance = self.object
                rules.save()
        return super().form_valid(form)


class AudienceDeleteView(DeleteView):
    model = Audience
    template_name = 'dashboard/audience/audience_confirm_delete.html'
    success_url = reverse_lazy('audience-list')


class RuleInlineFormSet(
    inlineformset_factory(Audience, Rule, fields=('condition', 'filter', 'operator'), extra=1)):
    pass
