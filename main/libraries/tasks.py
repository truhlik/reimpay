from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.translation import ugettext as _


def send_email(subject, email_from, email_to, text_content=None, html_content=None,
               attachments=None, fail_silently=False, reply_to=list):
    """
    Sends html or plain emails depending on which content is given, attachments must be
    instance of permissions.models.EmailAttachment

    :param subject: String subject of the email
    :param email_to: Email address of the addressee or list of emails
    :param email_from: Email address of the sender
    :param text_content: Plain email content (send only if html_content not given)
    :param html_content: HTML formatted content (send only if text_content not given)
    :param attachments: EmailAttachment object or list of them
    :param fail_silently: Boolean defining if error should be raised in case of fail
    :param reply_to: list of reply to recipients
    """

    if not isinstance(email_to, list):
        email_to = [email_to]

    if html_content and not text_content:
        text_content = strip_tags(html_content)
    elif text_content and not html_content:
        pass
    else:   # neither text nor html content or both
        raise ImproperlyConfigured("Either text_content or html_content must be given.")

    msg = EmailMultiAlternatives(
        str(subject),
        text_content,
        str(email_from),
        email_to,
        reply_to=reply_to,
    )

    if html_content:
        msg.attach_alternative(html_content, "text/html")

    if attachments:
        from .models import EmailAttachment

        if not isinstance(attachments, list):
            attachments = [attachments]

        for attachment in attachments:
            try:
                if isinstance(attachment, EmailAttachment):
                    msg.attach_file(attachment.path, attachment.mimetype)
            except IOError:
                pass

    return msg.send(fail_silently=fail_silently)


# To use it as a task, the celery must be installed and celery_app.py imported to enable self.retry
# To really send SMS django-smsbrana must be installed, otherwise sms is sent as a email of the user
# @celery_app.task(bind=True, default_retry_delay=60, max_retries=5)
# def send_sms(phone, email_from, email_to, text, fail_silently=False):
#     """
#     Manages SMS sending - sends SMS to given phone number or email if settings.DEBUG or settings.SEND_SMS=False
#     :param phone: Phone number of the recipient
#     :param email_from: Email sender in case email is sent instead of sms
#     :param email_to: Email recipient (notified user) in case email is sent instead of sms
#     :param text: Text message
#     :param fail_silently: Boolean defining if error should be raised in case of fail passed to send_email function
#     :return:
#     """
#     if (settings.DEBUG or not settings.SEND_SMS) and phone:
#         send_sms_as_email(phone, email_from, email_to, text, fail_silently=fail_silently)
#
#     elif phone and settings.SMS_ENABLED:
#
#         from smsbrana import SmsConnect, SmsConnectException    # maybe move to try as well
#
#         try:
#             sc = SmsConnect()
#             if len(text) > settings.SMS_MAX_CHARACTERS:
#                 text = text[:settings.SMS_MAX_CHARACTERS - 1]
#                 text = unidecode(text)
#                 text.encode('ascii')
#             result = sc.send_sms(message=text, number=str(phone))
#
#             # if not result:
#             #     raise self.retry()
#
#         except (SmsConnectException, ConnectionError):
#             pass
#             # raise self.retry()


def send_sms_as_email(phone, email_from, email_to, text, fail_silently=False):
    """
    Sends emails instead of SMS messages
    :param phone: Phone number of the SMS recipient
    :param email_from: Email sender in case email is sent instead of sms
    :param email_to: Email recipient (notified user) in case email is sent instead of sms
    :param text: Text message
    :param fail_silently: Boolean defining if error should be raised in case of fail passed to send_email function
    :return:
    """
    subject = _(u'SMS pro číslo: ') + str(phone)
    text = _(u'Tento email slouží jako náhrada SMS odeslané na číslo: ') + str(phone) + _(u' s obsahem:\n\n') + text

    return send_email(subject, email_from, email_to, text, fail_silently=fail_silently)
