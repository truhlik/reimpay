from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from rest_framework.views import APIView
from wkhtmltopdf.views import PDFTemplateResponse


class ApiPdfTemplateView(TemplateResponseMixin, ContextMixin, APIView):
    """ Celá implementace vychází z wkhtml.PDFTemplateView """

    # Filename for downloaded PDF. If None, the response is inline.
    filename = 'rendered_pdf.pdf'

    # Send file as attachement. If True render content in the browser.
    show_content_in_browser = False

    # Filenames for the content, header, and footer templates.
    template_name = None
    header_template = None
    footer_template = None
    cover_template = None

    # TemplateResponse classes for PDF and HTML
    response_class = PDFTemplateResponse
    html_response_class = TemplateResponse

    # Command-line options to pass to wkhtmltopdf
    cmd_options = {
        # 'orientation': 'portrait',
        # 'collate': True,
        # 'quiet': None,
    }

    def __init__(self, *args, **kwargs):
        super(ApiPdfTemplateView, self).__init__(*args, **kwargs)

        # Copy self.cmd_options to prevent clobbering the class-level object.
        self.cmd_options = self.cmd_options.copy()

    def get(self, request, *args, **kwargs):
        response_class = self.response_class
        try:
            if request.GET.get('as', '') == 'html':
                # Use the html_response_class if HTML was requested.
                self.response_class = self.html_response_class
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        finally:
            # Remove self.response_class
            self.response_class = response_class

    def get_filename(self):
        return self.filename

    def get_cmd_options(self):
        return self.cmd_options

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a PDF response with a template rendered with the given context.
        """
        filename = response_kwargs.pop('filename', None)
        cmd_options = response_kwargs.pop('cmd_options', None)

        if issubclass(self.response_class, PDFTemplateResponse):
            if filename is None:
                filename = self.get_filename()

            if cmd_options is None:
                cmd_options = self.get_cmd_options()

            return super(ApiPdfTemplateView, self).render_to_response(
                context=context, filename=filename,
                show_content_in_browser=self.show_content_in_browser,
                header_template=self.header_template,
                footer_template=self.footer_template,
                cmd_options=cmd_options,
                cover_template=self.cover_template,
                **response_kwargs
            )
        else:
            return super(ApiPdfTemplateView, self).render_to_response(
                context=context,
                **response_kwargs
            )
