from django.db import models
from datetime import datetime

# Create your models here.

class effContractDetail(models.Model):
    period = models.IntegerField(verbose_name='งวดที่')
    due_date = models.DateField(null=True, blank=True, verbose_name='วันครบกำหนดชำระ')
    due_days = models.DateField(null=True, blank=True, verbose_name='จำนวนวันที่ครบกำหนดชำระ')

    installment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดชำระงวด')
    principal_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดเงินต้นคงเหลือ')
    principal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดเงินต้นที่ชำระมา')
    interest = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ดอกเบี้ย')
    # fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ค่าธรรมเนียม')
    # net_principal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดเงินต้นสุทธิหลังจ่าย')

    # cover_date = models.DateField(null=True, blank=True)
    # cover_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดชำระเงิน')
    payment_date = models.DateField(null=True, blank=True, verbose_name='วันที่ชำระเงิน')
    payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดชำระเงิน')

    # principal_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดเงินต้นที่ชำระแล้ว')
    # interest_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ดอกเบี้ยที่ชำระแล้ว')
    # fee_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ค่าธรรมเนียมที่ชำระแล้ว')

    # arletter_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='รหัสจดหมายทวงถาม')
    # collection_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ค่าทวงถามหนี้ทั้งหมด')

    # created_at = models.DateTimeField(auto_now_add=True, verbose_name='สร้างเมื่อ')
    # updated_at = models.DateTimeField(auto_now=True, verbose_name='อัปเดตเมื่อ')

    contract_detail_id = models.IntegerField(verbose_name='รหัสสัญญา')
    cont_no = models.CharField(max_length=100, null=True, blank=True, verbose_name='เลขที่สัญญา')
    cont_date = models.DateField(null=True, blank=True, verbose_name='วันที่เริ่มสัญญา')
    actual_date = models.DateField(null=True, blank=True, verbose_name='วันที่เริ่มต้นงวดจริง')

    # contract_detail = models.ForeignKey('ContractDetail', on_delete=models.CASCADE, related_name='payment_details')

    # สัญญาเงินกู้จะใช้ tb effcontractperiod ต้องมี eff ถ้าไม่มีจะเป็นเช่าซื้อ
    class Meta:
        db_table = 'LineOA_ViewEffContractPeriod'
        # ordering = ['card_no']
        managed = False

    def format_date(self, date_value):
        if date_value:
            date_str = str(date_value).strip()  # ลบช่องว่างที่อาจเกิดขึ้น

            try:
                # ตรวจสอบรูปแบบของวันที่ที่รับเข้ามา
                if "-" in date_str or len(date_str) == 10:  # ถ้าเป็นรูปแบบ "YYYY-MM-DD"
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')  
                elif len(date_str) == 8 and date_str.isdigit():  # ถ้าเป็น "YYYYMMDD"
                    date_obj = datetime.strptime(date_str, '%Y%m%d')
                else:
                    return "รูปแบบวันที่ไม่ถูกต้อง"

                return date_obj.strftime('%d/%m/%Y')  # แปลงเป็น DD/MM/YYYY

            except ValueError:
                return "ข้อมูลวันที่ไม่ถูกต้อง"
    
    #วันที่ครบกำหนดชำระ
    def duedate(self):
        return self.format_date(self.due_date)
    
    #วันที่ชำระเงิน
    def paymentday(self):
        return self.format_date(self.payment_date)
    
    def format_money(self, money):

        if money is not None:
            return f"{money:,.2f}"  # ใส่, กับ ทศนิยม 2 ตำแหน่ง
        return "ไม่มียอดคงเหลือ"
    
    #ยอดเงินต้นสุทธิหลังจ่าย
    # def net_principallll(self) :
    #     return self.format_money(self.net_principal)
    
    #ยอดเงินต้นคงเหลือก่อนชำระ
    def balancepricipal(self) :
        return self.format_money(self.principal_balance)
    
    #จำนวนยอดเงินต้นที่จ่ายแล้วล่าสุด
    def principaa(self) :
        return self.format_money(self.principal)
    
    #ยอดดอกเบี้ยสุทธิ
    def net_interest(self) :
        return self.format_money(self.interest)
    
    #ยอดที่ต้องชำระของงวดนั้น
    def installmente(self) :
        return self.format_money(self.installment)
    
    #ค่าธรรมเนียมที่ต้องชำระ
    # def fee_due(self) :
    #     return self.format_money(self.fee)
    
    #ยอดที่จ่ายมา
    def paymentt(self) :
        return self.format_money(self.payment)

    
