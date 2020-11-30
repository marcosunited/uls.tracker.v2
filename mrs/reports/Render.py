from io import BytesIO

from MySQLdb import Time
from django.template import Template

from xhtml2pdf import pisa

from mrs.models import Report, ReportHistory


def render_to_pdf(report_id, context_dict={}):
    try:
        report = Report.objects.get(id=report_id)
        template = Template(report.report_template)
        html = template.render(context_dict)
        content = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), content)

        if not pdf.err:
            report_history = ReportHistory.objects.get(reportId=report_id)
            report_history.finish_timestamp = Time.now
            report_history.result = 'OK'
            report_history.output_file.save(report.name + '_' +
                                            report_id + '_' +
                                            str(Time.now), content, save=True)
            report_history.save()
            return 'OK'
    except RuntimeError as e:
        print(e)
        return None
