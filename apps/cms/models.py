from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from simple_history.models import HistoricalRecords

from apps.core.models import BaseModel
from apps.users.models import User


class Category(BaseModel):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/')
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.email


class Content(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    excerpt = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=(
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ), default='draft')
    categories = models.ManyToManyField(Category, related_name='contents')
    tags = models.ManyToManyField(Tag, blank=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to='featured_images/')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    history = HistoricalRecords()

    class Meta:
        abstract = True


class Article(Content):
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='article_contents')

    def __str__(self):
        return self.title


class Page(Content):
    order = models.PositiveIntegerField(default=0, help_text='Display order in menu')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='page_contents')

    def __str__(self):
        return self.title


class Attachment(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='upload/')

    def __str__(self):
        return self.title


class Slider(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    auto_play = models.BooleanField(default=True)
    auto_play_speed = models.PositiveIntegerField(default=5000)
    show_controls = models.BooleanField(default=True)
    show_navigation = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SliderItem(BaseModel):
    TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('product', 'Product'),
        ('article', 'Article'),
    ]

    slider = models.ForeignKey(Slider, on_delete=models.CASCADE, related_name='items')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='image')
    image = models.ImageField(null=True, blank=True, upload_to='slider_images/')
    video = models.FileField(null=True, blank=True, upload_to='slider_videos/')
    # product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    article = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL)
    caption = models.CharField(max_length=200, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.slider.name} - Item {self.order}"
