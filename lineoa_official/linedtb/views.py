
from datetime import datetime, date
from decimal import Decimal
import locale
from django.shortcuts import render

from line_contractdetail.models import effContractDetail
from contractline_noteff.models import ContractPeriod
from .models import Contractpaymentdetail
from line_detailpayment.models import LineOA_contract

from line_detailpayment.models import Loan_Penalty_BOT, loan_penalty





from .forms import SearchForm
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.cache import never_cache

from django.db.models import Sum, Max


@csrf_exempt
@never_cache
def ContractInfoForm(request):
    form = SearchForm(request.POST or None)
    result = None
    context = {'form': form}

    if request.method == 'POST' and form.is_valid():
        card_num = form.cleaned_data['card_no']
        # print(card_num)
        # ดึงข้อมูล ContractInfo พร้อมดึงข้อมูลการชำระเงินที่เกี่ยวข้อง
        # result = ContractInfo.objects.filter(card_no = card_num).f
        # result_detail = ContractDetail.objects.filter(contract_id=re)
        # print(result)
        # for foo in result:
            # result2 = Contractpaymentdetail.objects.filter(contract_id = foo.id,contract_detail_id = foo.contract_detail_id)
        result2 = LineOA_contract.objects.filter(card_no=card_num)
        # print('จำนวนสัญญา',len(result2))
        contract_period = ''
        # i = 0
        result_detail_h = ''
        suminstallment = []
        # payment_data = []
        
        # for mi in result2:
        #     print('cont_no', mi.cont_no)
        #     payment_data.append( Contractpaymentdetail.objects.filter(contract_id=mi.id, contract_detail_id=mi.contract_detail_id))
        # print('payment_data', type(payment_data))


        for foo in result2:
            result3 = Contractpaymentdetail.objects.filter(contract_id=foo.id, contract_detail_id=foo.contract_detail_id, status='A',cont_type=foo.cont_type)
            sumpayment=result3.aggregate(
                payment=Sum('payment')
            )
            # print('97', foo.id, foo.contract_detail_id)
            if foo.cont_type == 'E':
                todayy = date.today()
                contract_period = loan_penalty(foo.id, todayy , foo.cont_type)
                # print('6',contract_period)
                sumpay =0
                paymey =0
                intr = 0
                oppp = 0
                for p in contract_period :
                    sumpay += p.installment
                    paymey += p.payment
                    oppp += p.principal
                    intr += p.interest
                # print('5',sumpay, paymey, oppp, intr)
                
            else:
                result_detail_h = ContractPeriod.objects.filter(contract_detail_id=foo.contract_detail_id)
                suminstallment = result_detail_h.aggregate(
                    installment=Sum('installment'),
                    payment=Sum('payment'),
                    intert = Sum('interest'),
                    v_instal = Sum('vat_installment'),
                    pricip = Sum('principal'),
                    pricip_b = Sum('principal_balance'),
                )
        # print('50', result3)


        # for foo2 in result3_calc:
        #     result_detail_e = effContractDetail.objects.filter(contract_detail_id=foo2.contract_detail_id)

            
        #     result_detail_h = ContractPeriod.objects.filter(contract_detail_id=foo2.contract_detail_id)
            # payment_list = Loan_Penalty_BOT.objects.filter(contract_id=foo.id, contract_detail_id=foo.id).order_by('id').aaggregate(
            #     payment=Sum('payment'),
            #     installment=Sum('installment'),
            # )
        locale.setlocale(locale.LC_TIME, "th_TH")
        today = datetime.now()
        now = today.strftime("%d %b %Y")
        context = {
            'form': form,
            #'result': result,
            'result2': result2 ,
            'result3': result3 ,
            # 'result_detail_e': result_detail_e,
            'contract_period' : contract_period,
            'result_detail_h': result_detail_h,
            # 'payment_list' : payment_list,
            'sumpayment' : sumpayment,
            'suminstallment' : suminstallment,
            'sumpay' : sumpay,
            'paymey' : paymey,
            'oppp' : oppp,
            'intr' : intr,
            # 'payment_data' : payment_data,
            # 'summary': summary,
            # 'result4': result4 ,
            # 'result5': result5 ,
            'now': now,
        }

    return render(request, 'search.html', context )

# def penalty_summary_view(request):
#     summary = Loan_Penalty_BOT.get_totals()  # หรือ get_totals(contract_detail_id=...)
#     print('3',summary)

#     return render(request, 'search.html', {'summary': summary})



# def penalty_summary_view(request):
   

#     summary = Loan_Penalty_BOT.objects.aggregate(
#         total_paid=Sum('payment'),
#         total_principal=Sum('principal'),
#         total_interest=Sum('interest'),
#         total_installment=Sum('installment')
#     )
    
#     return render(request, 'search.html', {'summary': summary})






