from background_task import background
from django.core.mail import EmailMessage
from django.template import Context, Template

from mrs.models import Report


@background(schedule=10)
def sendMail(subject, report_id, data, origin, to, attachment):
    template_text = Report.objects.get(id=report_id).report_template
    template = Template(template_text)
    mail_context = Context(data)
    content = template.render(mail_context)
    msg = EmailMessage(subject, content, origin, [to])
    msg.content_subtype = "html"
    msg.attach_file(attachment)
    msg.send()






