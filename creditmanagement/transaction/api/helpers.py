import uuid
from django.conf import settings
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import render_to_string



def render_to_pdf(template_src, context_dict={}):
    # template = get_template(template_src)
    # html  = template.render(context_dict)
    html = render_to_string(template_src, context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None









# def render_to_pdf(template_src, context_dict={}):
#     # template = get_template(template_src)
#     # html  = template.render(context_dict)
#     html = render_to_string(template_src, context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

#     # file_name = uuid.uuid4()
#     # try:
#     #     with open(str(settings.BASE_DIR) + f'/static/{file_name}.pdf', 'wb+') as output:
#     #         pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
#     # except Exception as e:
#     #     print(e)

#     if pdf.err:
#         return '', False
#     return file_name


    # if not pdf.err:
    #     return pdf
    #     # return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return None

    # file_name = uuid.uuid4()

    # try:
    #     with open(str(settings.BASE_DIR) + f'/static/{file_name}.pdf', 'wb+') as output:
    #         pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    # except Exception as e:
    #     print(e)


    # if pdf.err:
    #         return '', False
        
    # return file_name, True


# def save_pdf(params):
#     # template = get_template("pdf_convert/payment_summary.html")
#     html = render(params, 'pdf_convert/payment_summary.html')
#     print("html", html)
#     response = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
#     file_name = uuid.uuid4()

#     try:
#         with open(str(settings.BASE_DIR) + f'/static/{file_name}.pdf', 'wb+') as output:
#             pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
#     except Exception as e:
#         print(e)

#     if pdf.error:
#         return '', False
    
#     return file_name, True