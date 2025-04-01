# import requests
from datetime import datetime
import locale
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from linedtb.models import Contractpaymentdetail
# import tempfile
# from requests.structures import CaseInsensitiveDict
# from django.conf import settings

def generate_pdf(request):

    pay_no = request.GET.get('payment_no')
    pay_name = request.GET.get('payfor_name')

    pay = Contractpaymentdetail.objects.filter(payment_no=pay_no, payfor_name=pay_name, status='A')
    print(pay, '1')
    print(pay_no)
    print(pay_name)

    locale.setlocale(locale.LC_TIME, "th_TH")
    today = datetime.now()
    now = today.strftime("%d %b %Y")
    # pay3 = None
    # pay3 = Contractpaymentdetail.objects.filter(payment_no=pay_no,payment_date=pay_date,status='A').first()
    # html_string = render_to_string('payment.html', {
    #     'payment_no': '{{pay3.payment_no}}',
    #     'paydate': '{{pay3.paydate}}',
    # })
    context = {
        'pay': pay ,
        'now': now,

    }
    html_string = render_to_string('payment.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf_file = html.write_pdf()

    filename = f"Receipt_{pay_no}.pdf" if pay_no else "Receipt_unknown.pdf"
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

# def print_report(request):
#     report_server_string = settings.FR_SERVER
#     fr_headers = CaseInsensitiveDict()
#     fr_headers["Accept"] = "application/pdf"
#     fr_url = "{}://{}:{}/result?{}".format(
#         report_server_string['PROTOCOL'], 
#         report_server_string['HOST'], 
#         report_server_string['PORT'], 
#         request.META['QUERY_STRING'],)
#     try:
#         resp = requests.get(fr_url, headers=fr_headers)
#     except Exception as e:
#         return HttpResponseNotFound(e)
#     else:
#         resp_headers = resp.headers
#         response = HttpResponse(resp.content, content_type='application/pdf', )
#         response['Server'] = 'LMS Report Server'
#         response['Content-Disposition'] = resp_headers['Content-Disposition']
#         response['Cache-Control'] = resp_headers['Cache-Control']
#         response['Pragma'] = resp_headers['Pragma']
#         response['Accept-ranges'] = resp_headers['Accept-ranges']
#         response['Last-Modified'] = resp_headers['Last-Modified']
#         response['Expires'] = resp_headers['Expires']
#         response['X-Powered-By'] = resp_headers['X-Powered-By']
#         response['FastReport-container'] = resp_headers['FastReport-container']
#         return response
    

# def generate_receipt_pdf(request, payment_id):
    # #  เตรียมหัวข้อ API Header และข้อมูลที่ต้องส่งไป FastReport
    # headers = {
    #     "Authorization": f"Bearer {settings.FASTREPORT_API_TOKEN}",
    #     "Content-Type": "application/json"
    # }
    
    # report_request = {
    #     "report_id": settings.FASTREPORT_REPORT_ID,  # ระบุ Report ID ที่สร้างไว้
    #     "parameters": {
    #         "payment_id": payment_id  # ส่งค่า payment_id ไปให้ FastReport ใช้ดึงข้อมูลจากฐานข้อมูล
    #     },
    #     "exportFormat": "pdf"  # ขอไฟล์เป็น PDF
    # }

    # # 2. ส่งคำขอให้ FastReport Server สร้างไฟล์ PDF
    # response = requests.post(f"{settings.FASTREPORT_API_URL}/generate", headers=headers, json=report_request)

    # #  3. ตรวจสอบการสร้าง PDF
    # if response.status_code == 200:
    #     pdf_url = response.json().get("fileUrl")  # รับ URL ของ PDF จาก FastReport
        
    #     #  4. ดาวน์โหลดไฟล์ PDF จาก FastReport Server
    #     pdf_response = requests.get(pdf_url, headers=headers)
        
    #     if pdf_response.status_code == 200:
    #         #  5. ส่งไฟล์ PDF กลับไปให้ผู้ใช้ดาวน์โหลดทันที
    #         pdf_filename = f"receipt_{payment_id}.pdf"
    #         http_response = HttpResponse(pdf_response.content, content_type="application/pdf")
    #         http_response["Content-Disposition"] = f'attachment; filename="{pdf_filename}"'
    #         return http_response
    #     else:
    #         return JsonResponse({"error": "ไม่สามารถดาวน์โหลด PDF ได้"}, status=500)

    # return JsonResponse({"error": "FastReport ไม่สามารถสร้าง PDF ได้"}, status=500)

