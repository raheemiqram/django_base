from django.urls import path
from .views import AudienceListView, AudienceCreateView, AudienceUpdateView
urlpatterns = [
    path('audiences/', AudienceListView.as_view(), name='audience-list'),
    path('audiences/create/', AudienceCreateView.as_view(), name='audience-create'),
    path('audiences/<int:pk>/update/', AudienceUpdateView.as_view(), name='audience-update'),
]