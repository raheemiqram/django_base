from django.db import models
from django.utils.translation import gettext_lazy as _


class AuthenticationMethod(models.TextChoices):
    EMAIL = "email", _("Email")
    USERNAME = "username", _("Username")
    USERNAME_EMAIL = "username_email", _("Username Email")


class AudienceFilter(models.TextChoices):
    ALL_CUSTOMER = "all_customer", _("All Customer")
    CUSTOM_CUSTOMER = "custom_customer", _("Custom Customer")
    NAME = "name", _("Name")
    EMAIL = "email", _("Email")
    COUNTRY = "country", _("Country")
    IS_SUPER_ADMIN = "is_super_user", _("is Super User")
    IS_STAFF = "is_staff", _("Is Staff")


class AudienceOperator(models.TextChoices):
    EQUAL = "equal", _("Equal")
    CONTAINS = "icontains", _("Contains")
    IN = "in", _("In")
    GRATER_THAN = "gt", _("Grater than")
    GRATER_THAN_EQUAL = "gte", _("Grater than equal")
    LESS_THAN = "lt", _("Less than")
    LESS_THAN_EQUAL = "lte", _("Less than equal")
    START_WITH = "startswith", _("Start with")
    RANGE = "range", _("Range")
    EXISTS = "exist", _("Exist")


class CampaignChannel(models.TextChoices):
    EMAIL = "email", _("Email")
    SMS = "sms", _("SMS")
    PUSH = "push", _("Push")


class CampaignStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    INITIATED = "initiated", _("Initiated")
    SENT = "sent", _("Sent")
    FAIL = "fail", _("Fail")


class CampaignType(models.TextChoices):
    MANUAL = "manual", _("Manual")
    AUTO = "auto", _("Auto")


class TemplateType(models.TextChoices):
    EMAIL = "email", _("Email")
    SMS = "sms", _("SMS")
    PUSH = "push", _("Push")


class TemplateFormatType(models.TextChoices):
    GENERAL = "general", _("General")
    PERSONALIZED = "personalized", _("Personalized")


class NotificationType(models.TextChoices):
    EMAIL = "email", _("Email")
    SMS = "sms", _("SMS")
    PUSH = "push", _("Push")


class NotificationStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    SENT = "sent", _("Sent")
    FAIL = "failed", _("Failed")