from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


class Mailer:

    def __init__(self, subject, template, data, origin, to, attachment):
        self.subject = subject
        self.template = template
        self.data = data
        self.origin = origin
        self.to = to
        self.attachment = attachment

    def sendMail(self):
        plain_text = get_template(self.template + '.txt')
        html = get_template(self.template + '.html')
        mail_context = Context(self.data)
        text_content = plain_text.render(mail_context)
        html_content = html.render(mail_context)
        msg = EmailMultiAlternatives(self.subject, html_content, self.origin, [self.to])
        msg.content_subtype = "html"
        msg.attach_alternative(text_content, "text/plain")
        msg.attach_file(self.attachment)
        msg.send()






