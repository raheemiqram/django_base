from django.urls import path, include

from apps.dashboard.tables.article_tables import ArticleAjaxDatatableView
from apps.dashboard.tables.attachment_tables import AttachmentAjaxDatatableView
from apps.dashboard.tables.audience_tables import AudienceAjaxDatatableView
from apps.dashboard.tables.page_tables import PageAjaxDatatableView
from apps.dashboard.tables.slider_tables import SliderAjaxDatatableView
from apps.dashboard.tables.template_tables import TemplateAjaxDatatableView
from apps.dashboard.tables.user_tables import UserAjaxDatatableView
from apps.dashboard.views import DashboardIndexView, DashboardEmptyView, DashboardLoginView

urlpatterns = [
    # ...
    path('', DashboardIndexView.as_view(), name='dashboard_index'),
    path('empty/', DashboardEmptyView.as_view(), name='dashboard_empty'),
    path('bots/', include('apps.chat_bot.urls')),
    path('cms/', include('apps.cms.urls')),
    path('configuration/', include('apps.core.urls')),
    path('messaging/', include('apps.messaging.urls')),
    path('marketing/', include('apps.marketing.urls')),
    path('trading/', include('apps.trading_bot.urls')),
    # ...

    # LOGIN
    path('login/', DashboardLoginView.as_view(), name='dashboard_login'),

    # TABLES
    path('table/users/', UserAjaxDatatableView.as_view(), name='dashboard_user_table'),
    path('table/articles/', ArticleAjaxDatatableView.as_view(), name='dashboard_articles_table'),
    path('table/pages/', PageAjaxDatatableView.as_view(), name='dashboard_pages_table'),
    path('table/sliders/', SliderAjaxDatatableView.as_view(), name='dashboard_sliders_table'),
    path('table/attachment/', AttachmentAjaxDatatableView.as_view(), name='dashboard_attachment_table'),
    path('table/template/', TemplateAjaxDatatableView.as_view(), name='dashboard_template_table'),
    path('table/notification/', AttachmentAjaxDatatableView.as_view(), name='dashboard_notification_table'),
    path('table/audience/', AudienceAjaxDatatableView.as_view(), name='dashboard_audience_table'),
    path('table/campaign/', AttachmentAjaxDatatableView.as_view(), name='dashboard_campaign_table'),
    # ...

]
