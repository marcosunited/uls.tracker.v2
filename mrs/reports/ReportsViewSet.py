from django.http import JsonResponse
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView

from mrs.models import Report
from mrs.reports.Renderer import render_to_pdf
from mrs.reports.ReportsConf import reports_processors
from mrs.utils.response import ResponseHttp


class BinaryFileRenderer(BaseRenderer):
    media_type = 'application/octet-stream'
    format = None
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class ReportsView(APIView):
    renderer_classes = [BinaryFileRenderer]

    def get(self, request, report_id, model_pk):
        try:
            data = self.process_report(report_id, model_pk)
            pdf = render_to_pdf(report_id, model_pk, data)
            return Response(
                data=pdf['content'].getvalue(),
                headers={'Content-Disposition': 'attachment; filename=' + pdf['name']},
                content_type='application/pdf')
        except Exception as error:
            return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def process_report(self, report_id, model_pk):
        report = Report.objects.get(id=report_id)
        if report.report_processor in reports_processors:
            data = reports_processors[report.report_processor](report, model_pk)
            return data
        else:
            raise Exception("Processor %s not implemented" % report.report_processor)
