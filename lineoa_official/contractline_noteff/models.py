from django.db import models
from datetime import datetime

# Create your models here.
class ContractPeriod(models.Model):
    period = models.IntegerField(verbose_name='งวดที่')
    due_date = models.DateField(null=True, blank=True, verbose_name='วันครบกำหนดชำระ')
    due_days = models.IntegerField(null=True, blank=True, verbose_name='จำนวนวันครบกำหนดชำระ')

    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='อัตราภาษีมูลค่าเพิ่ม')
    installment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดชำระงวด')
    # net_installment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดชำระสุทธิ')
    vat_installment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ภาษีจากยอดชำระ')

    principal_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='เงินต้นคงเหลือ')
    principal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='เงินต้น')
    interest = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ดอกเบี้ย')
    # fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ค่าธรรมเนียม')
    # net_principal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='เงินต้นสุทธิ')

    # straight_line_principal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='เงินต้นตามวิธีเส้นตรง')
    # straight_line_interest = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ดอกเบี้ยตามวิธีเส้นตรง')
    # straight_line_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ค่าธรรมเนียมตามวิธีเส้นตรง')

    # cover_date = models.DateField(null=True, blank=True, verbose_name='วันที่รับชำระเงิน')
    # cover_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดรับชำระเงิน')

    payment_date = models.DateField(null=True, blank=True, verbose_name='วันที่ชำระ')
    payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดชำระ')
    # net_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดชำระสุทธิ')
    # vat_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ภาษีที่ชำระ')

    # principal_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='เงินต้นที่ชำระแล้ว')
    # interest_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ดอกเบี้ยที่ชำระแล้ว')
    # fee_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ค่าธรรมเนียมที่ชำระแล้ว')

    # straight_line_principal_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='เงินต้นที่ชำระแล้วตามเส้นตรง')
    # straight_line_interest_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ดอกเบี้ยที่ชำระแล้วตามเส้นตรง')
    # straight_line_fee_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ค่าธรรมเนียมที่ชำระแล้วตามเส้นตรง')

    # net_installment_received = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดชำระสุทธิที่รับแล้ว')
    # vat_installment_received = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ภาษีจากยอดชำระที่รับแล้ว')
    # interest_received = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ดอกเบี้ยที่รับแล้ว')
    # fee_received = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ค่าธรรมเนียมที่รับแล้ว')

    # straight_line_interest_received = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ดอกเบี้ยที่รับแล้วตามเส้นตรง')
    # straight_line_fee_received = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ค่าธรรมเนียมที่รับแล้วตามเส้นตรง')

    # arletter_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='รหัสจดหมายทวงถาม')
    # collection_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='ยอดทวงถามหนี้ทั้งหมด')

    contract_detail_id = models.IntegerField(verbose_name='รหัสสัญญา')

    cont_no = models.CharField(max_length=100, null=True, blank=True, verbose_name='เลขที่สัญญา')
    cont_date = models.DateField(null=True, blank=True, verbose_name='วันที่เริ่มสัญญา')
    actual_date = models.DateField(null=True, blank=True, verbose_name='วันที่เริ่มต้นงวดจริง')
    customer_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='รหัสลูกค้า')

    class Meta:
        db_table = 'LineOA_ViewHireContractPeriod'
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
    def duedayy(self):
        return self.format_date(self.due_date)
    
    #วันที่ชำระเงิน
    def paymenttday(self):
        return self.format_date(self.payment_date)
    
    def format_money(self, money):

        if money is not None:
            return f"{money:,.2f}"  # ใส่, กับ ทศนิยม 2 ตำแหน่ง
        return "ไม่มียอดคงเหลือ"
    
    #เงินต้น
    def prici(self):
        return self.format_money(self.principal)
    
    #ดอกเบี้ย
    def inter(self):
        return self.format_money(self.interest)
    
    #ค่าธรรมเนียม
    # def feee(self):
    #     return self.format_money(self.fee)
    
    #ยอดภาษีมูลค่าเพิ่ม
    def instalmen(self):
        return self.format_money(self.vat_installment)
    
    #ยอดเงินต้นที่ต้องชำระ
    def installmenpay(self):
        return self.format_money(self.installment)
    
    #ยอดชำระสุทธิ
    def payma(self):
        return self.format_money(self.payment)
    
    #เงินต้นคงเหลือ
    def balance(self):
        return self.format_money(self.principal_balance)
    

    
