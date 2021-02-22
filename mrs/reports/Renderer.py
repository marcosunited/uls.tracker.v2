from io import BytesIO

from django.template import Template, Context

from xhtml2pdf import pisa

from mrs.models import Report


# TODO: set option to return pdf byte stream in the rest response and dont save
def render_to_pdf(report_id, model_pk, data_dict={}):
    try:
        report = Report.objects.get(id=report_id)
        template = Template(report.report_template)
        context = Context(data_dict)
        html = template.render(context)
        content = BytesIO()

        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), content)
        if not pdf.err:
            return {'content': content,
                    'name': report.name + "_" + report_id + "_" + model_pk + ".pdf"}

    except RuntimeError as e:
        print(e)
        return None
