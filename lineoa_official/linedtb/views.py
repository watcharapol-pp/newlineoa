# from django.shortcuts import render, get_object_or_404
# from .models import ContractInfo
# from django import forms


# # ฟอร์มสำหรับกรอกรหัสหรือเลขบัตรประชาชน
# class ContractInfoForm(forms.ModelForm):
#     class Meta:
#         model = ContractInfo
#         fields = '__all__'
#         contracts = ContractInfo.objects.order_by('idno')[:5]
#         # Loop through all ContractInfo objects and print their contract_id
#         for contract in contracts :
#             print(f"Contract No: {contract.CFSSNO}, Full Name: {contract.FULLNAME}, Status: {contract.STATUS}, Address: {contract.CFADDRESS},")
from datetime import datetime
import locale
from django.shortcuts import render
from .models import Contractpaymentdetail
from line_detailpayment.models import LineOA_contract

from .forms import SearchForm
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.cache import never_cache


@csrf_exempt
@never_cache
def ContractInfoForm(request):
    form = SearchForm(request.POST or None)
    result = None
    context = {'form': form}

    if request.method == 'POST' and form.is_valid():
        card_num = form.cleaned_data['card_no']
        print(card_num)

        # ดึงข้อมูล ContractInfo พร้อมดึงข้อมูลการชำระเงินที่เกี่ยวข้อง
        # result = ContractInfo.objects.filter(card_no = card_num).f
        # result_detail = ContractDetail.objects.filter(contract_id=re)
        # print(result)
        # for foo in result:
            # result2 = Contractpaymentdetail.objects.filter(contract_id = foo.id,contract_detail_id = foo.contract_detail_id)
        result2 = LineOA_contract.objects.filter(card_no=card_num)
        for foo in result2:
            result3 = Contractpaymentdetail.objects.filter(contract_id=foo.id, contract_detail_id=foo.contract_detail_id, status='A')
        print('2', result2, result3 )
        locale.setlocale(locale.LC_TIME, "th_TH")
        today = datetime.now()
        now = today.strftime("%d %b %Y")
        context = {
            #'result': result ,
            'result2': result2 ,
            'result3': result3 ,
            'now': now,
        }

    return render(request, 'search.html', context )




