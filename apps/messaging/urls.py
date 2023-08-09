from django.urls import path
from .views import TemplateListView, TemplateCreateView, TemplateUpdateView, TemplateDeleteView

urlpatterns = [
    path('template/', TemplateListView.as_view(), name='template_list'),
    path('template/create/', TemplateCreateView.as_view(), name='template_create'),
    path('template/<int:pk>/update/', TemplateUpdateView.as_view(), name='template_update'),
    path('template/<int:pk>/delete/', TemplateDeleteView.as_view(), name='template_delete'),
]
