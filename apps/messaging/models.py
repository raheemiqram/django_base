from django.db import models
from apps.core.enums import TemplateFormatType, TemplateType, NotificationType, NotificationStatus
from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _
from apps.users.models import User


class Template(BaseModel):
    title = models.CharField(max_length=500)
    body = models.TextField(blank=True)
    body_html = models.TextField(_("Email Body HTML Template"), blank=True)
    template_type = models.CharField(
        max_length=16, choices=TemplateType.choices, default=TemplateType.EMAIL
    )
    re_usable = models.BooleanField(default=True)
    template_format = models.CharField(
        max_length=16, choices=TemplateFormatType.choices, default=TemplateFormatType.GENERAL
    )

    # for push notification
    image_url = models.URLField(blank=True)
    trigger_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title}"


class Notification(BaseModel):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")

    # Not all notifications will have a sender.
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    notification_type = models.CharField(
        max_length=16, choices=NotificationType.choices, default=NotificationType.EMAIL
    )
    error_message = models.TextField(blank=True)
    body_html = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=NotificationStatus.choices, default=NotificationStatus.PENDING)

    # this will help to redirect the specific page when click the notification (Ex: navigate to order detail page)
    custom_detail_link = models.CharField(max_length=255, blank=True)
    campaign = models.ForeignKey("marketing.Campaign", blank=True, null=True, on_delete=models.CASCADE)

    # def send_notification(self, attachments=None, push_click_url=None, push_image_url=None):
    #
    #     if self.notification_type == NotificationType.EMAIL:
    #         try:
    #             from apps.communication.utils import Dispatcher
    #
    #             email_conn = get_connection()
    #             dispatch = Dispatcher(mail_connection=email_conn)
    #             dispatch.send_email_messages(
    #                 self.recipient.email,
    #                 {
    #                     "subject": self.subject,
    #                     "body": self.body,
    #                     "html": self.body_html,
    #                 },
    #                 self.sender.email if self.sender else dispatch.get_sender_email_address() or "info@kmmrce.com",
    #                 attachments=attachments,
    #             )
    #             self.status = NotificationStatus.SENT
    #             self.error_message = ""
    #         except Exception as e:
    #             self.error_message = f'Request error: "{str(e).capitalize()}".'
    #             self.status = NotificationStatus.FAIL
    #             self.save()
    #             raise Exception(f'Request error: "{str(e).capitalize()}".')
    #
    #     elif self.notification_type == NotificationType.SMS:
    #         try:
    #             client = get_twilio_client()
    #             if self.recipient.phone_number:
    #                 client.messages.create(
    #                     from_=settings.TWILIO_FROM_NUMBER,
    #                     body=self.body,
    #                     to=str(self.recipient.phone_number),
    #                 )
    #                 self.status = NotificationStatus.SENT
    #                 self.error_message = ""
    #             else:
    #                 self.status = NotificationStatus.FAIL
    #                 self.error_message = "User dose not have mobile number"
    #
    #         except Exception as e:
    #             self.error_message = f'Request error: "{str(e).capitalize()}".'
    #             self.status = NotificationStatus.FAIL
    #             self.save()
    #             raise Exception(f'Request error: "{str(e).capitalize()}".')
    #
    #     elif self.notification_type == NotificationType.PUSH:
    #         # one user has multiple devices ( chrome , firefox , android ,  i phone , etc)
    #         devices = FCMDevice.objects.filter(user=self.recipient, active=True)
    #         if devices:
    #             try:
    #                 from firebase_admin.messaging import Notification, Message
    #
    #                 for device in devices:
    #                     device.send_message(
    #                         Message(
    #                             notification=Notification(
    #                                 title=self.subject,
    #                                 body=self.body,
    #                                 image=push_image_url,
    #                             ),
    #                             data={"clickUrl": f"{push_click_url if push_click_url else '/'}"},
    #                         )
    #                     )
    #                 self.status = NotificationStatus.SENT
    #                 self.error_message = ""
    #             except Exception as e:
    #                 self.error_message = f'Request error: "{str(e).capitalize()}".'
    #                 self.status = NotificationStatus.FAIL
    #                 self.save()
    #                 raise Exception(f'Request error: "{str(e).capitalize()}".')
    #         else:
    #             self.error_message = f"{self.recipient} does not have device id."
    #             self.status = NotificationStatus.FAIL
    #             self.save()
    #     else:
    #         raise NotImplementedError
    #
    #     self.save()
