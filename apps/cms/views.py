from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Article, Page, Slider, SliderItem, Attachment


class ArticleListView(ListView):
    model = Article
    template_name = 'dashboard/cms/articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'dashboard/cms/articles/article_detail.html'
    context_object_name = 'article'


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'dashboard/cms/articles/article_form.html'
    fields = ['title', 'subtitle', 'slug', 'body', 'excerpt', 'status', 'categories', 'tags',
              'featured_image']
    success_url = reverse_lazy('article_list')


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'dashboard/cms/articles/article_form.html'
    fields = ['title', 'subtitle', 'slug', 'body', 'excerpt', 'status', 'categories', 'tags',
              'featured_image']
    success_url = reverse_lazy('article_list')


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('article_list')


class PageListView(ListView):
    model = Page
    template_name = 'dashboard/cms/pages/page_list.html'
    context_object_name = 'pages'
    paginate_by = 10


class PageDetailView(DetailView):
    model = Page
    template_name = 'dashboard/cms/pages/page_detail.html'
    context_object_name = 'page'


class PageCreateView(CreateView):
    model = Page
    template_name = 'dashboard/cms/pages/page_form.html'
    fields = ['title', 'slug', 'body', 'excerpt', 'status', 'categories', 'tags', 'featured_image', 'parent',
              'order']
    success_url = reverse_lazy('page_list')


class PageUpdateView(UpdateView):
    model = Page
    template_name = 'dashboard/cms/pages/page_form.html'
    fields = ['title', 'slug', 'body', 'excerpt', 'status', 'categories', 'tags', 'featured_image', 'parent',
              'order']
    success_url = reverse_lazy('page_list')


class PageDeleteView(DeleteView):
    model = Page
    template_name = 'dashboard/cms/pages/page_confirm_delete.html'
    success_url = reverse_lazy('page_list')


class SliderListView(ListView):
    model = Slider
    template_name = 'dashboard/cms/sliders/slider_list.html'
    context_object_name = 'sliders'


class SliderDetailView(DetailView):
    model = Slider
    template_name = 'dashboard/cms/sliders/slider_detail.html'
    context_object_name = 'slider'


class SliderCreateView(CreateView):
    model = Slider
    template_name = 'dashboard/cms/sliders/slider_form.html'
    fields = ['name', 'slug', 'auto_play', 'auto_play_speed', 'show_controls', 'show_navigation']
    success_url = reverse_lazy('slider_list')


class SliderUpdateView(UpdateView):
    model = Slider
    template_name = 'dashboard/cms/sliders/slider_form.html'
    fields = ['name', 'slug', 'auto_play', 'auto_play_speed', 'show_controls', 'show_navigation']
    success_url = reverse_lazy('slider_list')


class SliderDeleteView(DeleteView):
    model = Slider
    template_name = 'dashboard/cms/sliders/slider_confirm_delete.html'
    success_url = reverse_lazy('slider_list')


class SliderItemListView(ListView):
    model = SliderItem
    template_name = 'slideitem_list.html'
    context_object_name = 'slide_items'


class SliderItemDetailView(DetailView):
    model = SliderItem
    template_name = 'slideitem_detail.html'
    context_object_name = 'slide_item'


class SliderItemCreateView(CreateView):
    model = SliderItem
    template_name = 'slideitem_form.html'
    fields = ['slider', 'title', 'subtitle', 'link', 'image', 'order']
    success_url = reverse_lazy('slideitem_list')


class SliderItemUpdateView(UpdateView):
    model = SliderItem
    template_name = 'slideitem_form.html'
    fields = ['slider', 'title', 'subtitle', 'link', 'image', 'order']
    success_url = reverse_lazy('slideitem_list')


class SliderItemDeleteView(DeleteView):
    model = SliderItem
    template_name = 'slideitem_confirm_delete.html'
    success_url = reverse_lazy('slideitem_list')


class AttachmentListView(ListView):
    model = Attachment
    template_name = 'dashboard/cms/attachment/attachment_list.html'


class AttachmentCreateView(CreateView):
    model = Attachment
    template_name = 'dashboard/cms/attachment/attachment_form.html'
    fields = ['title', 'description', 'file']
    success_url = reverse_lazy('attachment_list')
