from django.urls import path
from .views import ConfigurationCreateView, ConfigurationUpdateView, ConfigurationView

urlpatterns = [
    path('', ConfigurationView.as_view(), name='configuration_view'),
    path('create/', ConfigurationCreateView.as_view(), name='configuration_create'),
    path('<int:pk>/update/', ConfigurationUpdateView.as_view(), name='configuration_update'),
]
