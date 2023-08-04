import logging
from django.db import models
from django.db.models import Q
from apps.core.enums import AudienceFilter, AudienceOperator, CampaignStatus, CampaignType, TemplateFormatType, \
    NotificationType
from apps.core.models import BaseModel, Configuration
from apps.marketing.utils import get_filter, render_notification_template
from apps.messaging.models import Notification
from apps.users.models import User
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Audience(BaseModel):
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    last_execute_count = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.name

    def execute(self):
        rules = Rule.objects.filter(audience_id=self.id)
        filter_data = []
        for i in rules:
            data = {
                "condition": i.condition,
                "filter_name": i.filter,
                "filter_operator": i.operator,
                "filter_value": i.value,
            }
            filter_data.append(data)

        customer = User.objects.all()
        filter_objects = Q()
        for data in filter_data:
            if data["condition"] == "AND":
                filter_objects &= get_filter(data["filter_name"], data["filter_operator"], data["filter_value"])
            else:
                filter_objects |= get_filter(data["filter_name"], data["filter_operator"], data["filter_value"])

        queryset = customer.filter(filter_objects).distinct()
        self.last_execute_count = queryset.count()
        self.save()
        return queryset


class Rule(BaseModel):
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE)
    condition = models.CharField(max_length=3, choices=(("OR", "OR"), ("AND", "AND")), default="AND")
    filter = models.CharField(max_length=50, choices=AudienceFilter.choices)
    value = models.TextField(blank=True)
    operator = models.CharField(max_length=255, choices=AudienceOperator.choices)

    def __str__(self):
        return self.filter


class Campaign(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True)
    status = models.CharField(
        max_length=16, choices=CampaignStatus.choices, blank=True, default=CampaignStatus.INITIATED
    )
    type = models.CharField(
        choices=CampaignType.choices,
        blank=True,
        max_length=16,
        default=CampaignType.AUTO,
        help_text=_("If select manual need to set user ids(comma separated) in manual values "),
    )
    total_audience = models.IntegerField(blank=True, default=0)
    total_execute_audience = models.IntegerField(blank=True, default=0)
    audience = models.ForeignKey(Audience, null=True, blank=True, on_delete=models.SET_NULL)
    email_template = models.ForeignKey(
        "messaging.Template", blank=True, null=True, on_delete=models.SET_NULL, related_name="email_template"
    )
    sms_template = models.ForeignKey(
        "messaging.Template", blank=True, null=True, on_delete=models.SET_NULL, related_name="sms_template"
    )
    push_template = models.ForeignKey(
        "messaging.Template", blank=True, null=True, on_delete=models.SET_NULL, related_name="push_template"
    )
    manual_values = models.TextField(blank=True, help_text=_("manual values should be comma separated"))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.total_audience:
            self.total_audience = self.get_campaign_user().count()
        super().save(*args, **kwargs)

    def get_campaign_user(self):

        if self.type == CampaignType.AUTO:
            return self.audience.execute()
        elif self.type == CampaignType.MANUAL:
            return User.objects.filter(id__in=list(map(int, self.manual_values.split(","))))
        else:
            raise NotImplementedError

    def get_template_data(self, template, user):
        site = Configuration.objects.all()[0]
        # user last order
        title = template.title
        body = template.body
        body_html = template.body_html
        if template.template_format == TemplateFormatType.PERSONALIZED:
            title = render_notification_template(title, dict(user=user, site=site))
            body = render_notification_template(body, dict(user=user, site=site))
            body_html = render_notification_template(
                body_html, dict(user=user, site=site)
            )

        return title, body, body_html

    def execute_campaign(self):
        """
        this function will send notification according the configuration
        execute with asynchronous task for large data

        if its template format is personalized then template will change in runtime according to set inside
        the template
        for Ex:
        if you need customer name each template then client will define {{user.email}} in the template
        or site objects  - in the template  {{site.logo}}, or
        set like this inside the dict
        "render_notification_template(body, dict(user=user, site=site , etc ..))"
        """
        if not (self.email_template or self.sms_template or self.push_template):
            raise Exception("Template is required for campaign")
        if self.status == CampaignStatus.INITIATED:
            self.total_audience = self.get_campaign_user().count()
            self.total_execute_audience = 0
            self.status = CampaignStatus.PENDING
            self.save()
            for user in self.get_campaign_user():
                if self.email_template:
                    subject, body, body_html = self.get_template_data(self.email_template, user)
                    notification = Notification.objects.create(
                        recipient=user,
                        subject=subject,
                        body=body,
                        body_html=body_html,
                        notification_type=NotificationType.EMAIL,
                        campaign=self,
                    )
                    try:
                        notification.send_notification()
                    except Exception as e:
                        logger.debug(f"{e}")  # no error sent to sentry
                if self.sms_template:
                    subject, body, body_html = self.get_template_data(self.sms_template, user)
                    notification = Notification.objects.create(
                        recipient=user,
                        subject=subject,
                        body=body,
                        notification_type=NotificationType.SMS,
                        campaign=self,
                    )
                    try:
                        notification.send_notification()
                    except Exception as e:
                        logger.debug(f"{e}")  # no error sent to sentry
                if self.push_template:
                    subject, body, body_html = self.get_template_data(self.push_template, user)
                    notification = Notification.objects.create(
                        recipient=user,
                        subject=subject,
                        body=body,
                        notification_type=NotificationType.PUSH,
                        campaign=self,
                    )
                    try:
                        notification.send_notification()
                    except Exception as e:
                        logger.debug(f"{e}")  # no error sent to sentry
                self.total_execute_audience = self.total_execute_audience + 1
                self.save()

            self.status = CampaignStatus.SENT
            self.save()
        else:
            raise Exception("Campaign executed already")
