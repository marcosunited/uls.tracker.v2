from mrs.reports.Renderer import render_to_pdf
from mrs.reports.ReportsConf import reports_processors

processor = 'test'
if processor in reports_processors:
    context = reports_processors[processor]()
    render_to_pdf(1, context)
else:
    raise Exception("Processor %s not implemented" % processor)
