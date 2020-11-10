from background_task import background
from django.core.mail import EmailMessage
from django.template import Context, Template

from mrs.models import ContentTemplate


@background(schedule=60)
def sendMail(subject, template_name, data, origin, to, attachment):
    template_text = ContentTemplate.objects.get(name=template_name).content
    template = Template(template_text)
    mail_context = Context(data)
    content = template.render(mail_context)
    msg = EmailMessage(subject, content, origin, [to])
    msg.content_subtype = "html"
    msg.attach_file(attachment)
    msg.send()






