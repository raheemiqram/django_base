from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    PageListView,
    PageDetailView,
    PageCreateView,
    PageUpdateView,
    PageDeleteView,
    SliderListView,
    SliderDetailView,
    SliderCreateView,
    SliderUpdateView,
    SliderDeleteView, SliderItemCreateView, SliderItemUpdateView, SliderItemDeleteView, AttachmentListView,
    AttachmentCreateView
)

urlpatterns = [
    # Article URLs
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<slug:slug>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('articles/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),

    # Page URLs
    path('pages/', PageListView.as_view(), name='page_list'),
    path('pages/<int:pk>/', PageDetailView.as_view(), name='page_detail'),
    path('pages/create/', PageCreateView.as_view(), name='page_create'),
    path('pages/<slug:slug>/update/', PageUpdateView.as_view(), name='page_update'),
    path('pages/<slug:slug>/delete/', PageDeleteView.as_view(), name='page_delete'),

    # Slider URLs
    path('sliders/', SliderListView.as_view(), name='slider_list'),
    path('sliders/<int:pk>/', SliderDetailView.as_view(), name='slider_detail'),
    path('sliders/create/', SliderCreateView.as_view(), name='slider_create'),
    path('sliders/<slug:slug>/update/', SliderUpdateView.as_view(), name='slider_update'),
    path('sliders/<slug:slug>/delete/', SliderDeleteView.as_view(), name='slider_delete'),

    # SliderItem URLs
    path('sliders/<slug:slider_slug>/slideitems/create/', SliderItemCreateView.as_view(), name='slideritem_create'),
    path('sliders/<slug:slider_slug>/slideitems/<int:pk>/update/', SliderItemUpdateView.as_view(),
         name='slideritem_update'),
    path('sliders/<slug:slider_slug>/slideitems/<int:pk>/delete/', SliderItemDeleteView.as_view(),
         name='slideritem_delete'),

    path('attachments/', AttachmentListView.as_view(), name='attachment_list'),
    path('attachments/new/', AttachmentCreateView.as_view(), name='attachment_new'),

]
