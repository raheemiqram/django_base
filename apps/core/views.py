from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from apps.core.models import Configuration


class ConfigurationView(TemplateView):
    template_name = 'dashboard/configuration/configuration.html'

    def dispatch(self, request, *args, **kwargs):
        if not Configuration.objects.exists():
            return redirect('configuration_create')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ConfigurationView, self).get_context_data()
        config = Configuration.objects.first()
        ctx['configuration'] = config
        config = Configuration()
        ctx['configuration_cache'] = config.cached_queryset
        fields = {}
        for field in config._meta.fields:
            if field.name not in ['id']:
                fields[field.verbose_name] = field.value_from_object(config)
        ctx['fields'] = fields
        return ctx


class ConfigurationCreateView(CreateView):
    model = Configuration
    template_name = 'dashboard/configuration/configuration_form.html'
    fields = ['openai_api_key', 'facebook_app_id', 'facebook_app_secret', 'facebook_access_token',
              'instagram_access_token',
              'twitter_api_key', 'twitter_api_secret_key', 'site_name', 'site_description', 'site_logo', 'site_email',
              'site_phone', 'site_address', 'site_favicon', 'site_header_image', 'site_footer_text',
              'site_twitter_handle', 'site_facebook_url', 'site_instagram_url', 'site_linkedin_url', 'site_youtube_url',
              'enable_cache', 'enable_notifications', 'default_language']

    success_url = reverse_lazy('configuration_view')

    def dispatch(self, request, *args, **kwargs):
        if Configuration.objects.exists():
            configuration = get_object_or_404(Configuration, pk=1)
            return redirect('configuration_update', pk=configuration.pk)
        return super().dispatch(request, *args, **kwargs)


class ConfigurationUpdateView(UpdateView):
    model = Configuration
    template_name = 'dashboard/configuration/configuration_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('configuration_view')
