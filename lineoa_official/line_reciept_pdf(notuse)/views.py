
import json
import requests
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from linedtb.models import Contractpaymentdetail

# โหลด Credentials จากไฟล์
with open("credentials.json", "r", encoding="utf-8") as f:
    CREDENTIALS = json.load(f)

# API Endpoint ของ Adobe
TOKEN_URL = "https://ims-na1.adobelogin.com/ims/token"


def get_access_token():
    """ ขอ Access Token โดยใช้ Client ID และ Secret จาก credentials.json """
    if not settings.ADOBE_CLIENT_ID or not settings.ADOBE_CLIENT_SECRET:
        return None

    data = {
        "client_id": settings.ADOBE_CLIENT_ID,
        "client_secret": settings.ADOBE_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": settings.ADOBE_SCOPES
    }

    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None

def test_adobe_credentials(request):
    return JsonResponse({
        "ADOBE_CLIENT_ID": settings.ADOBE_CLIENT_ID,
        "ADOBE_CLIENT_SECRET": settings.ADOBE_CLIENT_SECRET,
        "ADOBE_ORG_ID": settings.ADOBE_ORG_ID,
        "ADOBE_SCOPES": settings.ADOBE_SCOPES
    })

ADOBE_PDF_API_URL = "https://api.adobe.com/pdf/generate"

def generate_receipt_pdf(request, payment_id):

    # ✅ ดึงข้อมูลใบเสร็จจากฐานข้อมูล
    receipt = Contractpaymentdetail.objects.filter(payment_id=payment_id)
    if not receipt:
        return JsonResponse({"error": "ไม่พบข้อมูลใบเสร็จ"}, status=404)

    # ✅ สร้างโครงสร้าง JSON สำหรับ API (คล้ายกับโค้ดเก่า)
    pdf_data = {
        "title": "ใบเสร็จรับเงิน",
        "header": {
            "text": "ใบเสร็จรับเงิน",
            "align": "center",
            "fontSize": 18,
            "bold": True
        },
        "details": [
            {"text": f"เลขที่ใบเสร็จ: {payment_id}", "fontSize": 14},
            {"text": f"วันที่ชำระ: {receipt.first().paydate}", "fontSize": 14},
            {"text": f"ยอดรวม: {receipt.first().moneytotal} บาท", "fontSize": 14}
        ],
        "table": {
            "columns": ["ลำดับ", "รายละเอียด", "จำนวนเงิน (บาท)"],
            "rows": []
        }
    }

    # ✅ เพิ่มข้อมูลในตาราง (ลูปผ่าน `receipt`)
    for index, slip in enumerate(receipt, start=1):
        pdf_data["table"]["rows"].append([str(index), slip.payfor_name, f"{slip.moneytotal}"])

    # ✅ ส่งข้อมูลไปยัง API Adobe PDF
    headers = {
        "Authorization": f"Bearer {settings.ADOBE_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(ADOBE_PDF_API_URL, headers=headers, data=json.dumps(pdf_data), verify=False)

    # ✅ ตรวจสอบการสร้าง PDF
    if response.status_code == 200:
        pdf_url = response.json().get("pdf_url")
        return JsonResponse({"pdf_url": pdf_url})  # ✅ ส่งลิงก์ PDF กลับให้ผู้ใช้
    else:
        return JsonResponse({"error": "ไม่สามารถสร้าง PDF ได้"}, status=500)
