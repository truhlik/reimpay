from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import activate

from .functions import get_absolute_url
from .tasks import send_email


class EmailBase:
    subject = None
    template_name = None

    def __init__(self, *args, **kwargs):
        pass

    def get_context(self):
        return {
            'title': self.get_subject(),
            'site_url': get_absolute_url(),
        }

    def get_subject(self):
        return self.subject

    def get_html_content(self, context):
        return render_to_string(self.template_name, context)

    def send_html_email(self, email_to, context=None, attachments=None, fail_silently=False, reply_to=list):
        """
        Send marketing emails to user based on given email_type.
        :param email_to: email of the reciever
        :param context: dict, context to use in email template
        :param attachments: EmailAttachment object or list of them,
        :param fail_silently: Boolean defining if error should be raised in case of fail
        :param reply_to: list of reply to recipients
        :return: Boolean if sending was successful
        """

        # aktivujeme jazyk pro překlady
        activate('cs')

        # naplníme context
        if not context:
            context = {}
        context.update(self.get_context())

        # vyrenderujeme HTML
        html_content = self.get_html_content(context)

        # odešleme email
        return send_email(
            subject=self.get_subject(),
            email_from=settings.DEFAULT_FROM_EMAIL,
            email_to=email_to,
            attachments=attachments,
            html_content=html_content,
            fail_silently=fail_silently,
            reply_to=reply_to,
        )


class EmailTicket(EmailBase):
    subject = 'ticket',
    template_name = 'emails/email_ticket.html'

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        super(EmailTicket, self).__init__(*args, **kwargs)

    def get_subject(self):
        return "ticket #{}".format(self.obj.id)

    def get_context(self):
        ctx = super(EmailTicket, self).get_context()
        ctx.update({
            'obj': self.obj,
        })
        return ctx
