from django.urls import path
from .views import TemplateListView, TemplateCreateView, TemplateUpdateView, TemplateDeleteView

urlpatterns = [
    path('', TemplateListView.as_view(), name='template_list'),
    path('create/', TemplateCreateView.as_view(), name='template_create'),
    path('<int:pk>/update/', TemplateUpdateView.as_view(), name='template_update'),
    path('<int:pk>/delete/', TemplateDeleteView.as_view(), name='template_delete'),
]
