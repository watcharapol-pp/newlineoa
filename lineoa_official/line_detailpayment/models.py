from django.db import models
from datetime import datetime
from django.db.models import Sum


class Loan_Penalty_BOT(models.Model):
    contract_id = models.IntegerField(default=0, null=True, blank=True)
    contract_detail_id = models.IntegerField(default=0, null=True, blank=True)
    period_id = models.IntegerField(default=0, null=True, blank=True)
    period = models.IntegerField(default=0, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    due_days = models.IntegerField(default=0, null=True, blank=True)
    installment = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    principal_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    principal_effect = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    principal = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    interest = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    int_current = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    int_suspend = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    fee = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    cover_date = models.DateField(null=True, blank=True)
    cover_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    principal_paid = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    interest_paid = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    int_current_paid = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    int_suspend_paid = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    fee_paid = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    net_principal = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    penalty_day = models.IntegerField(default=0, null=True, blank=True)
    penalty_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    penalty_paid_date = models.DateField(null=True, blank=True)
    penalty_paid = models.DecimalField(max_digits=18, decimal_places=2, default=0, null=True, blank=True)
    record_type = models.CharField(max_length=1, default='D', null=True, blank=True)

    class Meta:
        managed = False

    

    

    def format_date(self, date_value):
        if date_value:
            date_str = str(date_value).strip()  # ลบช่องว่างที่อาจเกิดขึ้น

            try:
                # ตรวจสอบรูปแบบของวันที่ที่รับเข้ามา
                if "-" in date_str and len(date_str) == 10:  # ถ้าเป็นรูปแบบ "YYYY-MM-DD"
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')  
                elif len(date_str) == 8 and date_str.isdigit():  # ถ้าเป็น "YYYYMMDD"
                    date_obj = datetime.strptime(date_str, '%Y%m%d')
                else:
                    return "รูปแบบวันที่ไม่ถูกต้อง"

                return date_obj.strftime('%d/%m/%Y')  # แปลงเป็น DD/MM/YYYY

            except ValueError:
                return "ข้อมูลวันที่ไม่ถูกต้อง"

        return "ไม่มีข้อมูลวันที่"
    
    def format_money(self, money):

        if money is not None:
            return f"{money:,.2f}"  # ใส่, กับ ทศนิยม 2 ตำแหน่ง
        return "ไม่มียอดคงเหลือ"

    def paydate(self):
        return self.format_date(self.payment_date)
    
    #วันที่ครบกำหนดชำระ
    def duedayy(self):
        return self.format_date(self.due_date)
    
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
    # def instalmen(self):
    #     return self.format_money(self.vat_installment)
    
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
    
    #ยอดที่จ่ายมา
    def paymentt(self) :
        return self.format_money(self.payment)
    
    # def pay(self) :
    #     return self.format_money(self.payment)


# Create your models here.
class LineOA_contract(models.Model):

    # id = models.IntegerField(verbose_name='idประจำสัญญา')
    branch_id = models.IntegerField(verbose_name='idสำนักงาน')
    branch_code = models.CharField(max_length=50,verbose_name='รหัสประจำสำนักงาน')
    branch_name = models.CharField(max_length=50,verbose_name='ชื่อสำนักงาน')
    contract_detail_id = models.IntegerField(verbose_name='contractdetail')
    cont_type = models.CharField(max_length=50,verbose_name='ตัวอักษรประจำประเภทสัญญา')
    cont_type_name = models.CharField(max_length=50,verbose_name='ชื่อประเภทสัญญา')
    cont_no = models.CharField(max_length=50,verbose_name='เลขที่สัญญา')
    cont_date = models.DateField(max_length=50,verbose_name='วันเริ่มสัญญา')
    actual_date = models.DateField(verbose_name='วันเริ่มสัญญาจริง')
    cont_group_id = models.IntegerField(verbose_name='id ประเภทสินเชื่อ')
    cont_group_code = models.CharField(max_length=50,verbose_name='รหัสประเภทสินเชื่อ')
    cont_group_name = models.CharField(max_length=50 ,verbose_name='ชื่อประเภทสินเชื่อ')
    sequence_method = models.CharField(max_length=50 ,verbose_name='ลำดับอะไรสักอย่าง')
    ar_type = models.CharField(max_length=50, verbose_name='ประเภทบัญชีลูกหนี้')
    ar_type_name = models.CharField(max_length=50 ,verbose_name='ชื่อสัญญาบัญชีลูกหนี้')
    payment_terms = models.CharField(max_length=50 ,verbose_name='ตัวย่อประเภทการจ่าย')
    payment_terms_name = models.CharField(max_length=50 ,verbose_name='ชื่อประเภทการจ่าย')
    customer_id = models.IntegerField(verbose_name='id ลูกหนี้')
    customer_name = models.CharField(max_length=50 ,verbose_name='ชื่อลูกหนี้')
    card_no = models.CharField(max_length=20, unique=True, verbose_name='เลขบัตรประชาชน')
    mobile = models.CharField(max_length=15, verbose_name='เบอร์โทรศัพท์')
    customer_slug = models.SlugField(unique=True, verbose_name='Slug ลูกค้า')
    customer_address_id = models.IntegerField(verbose_name='รหัสที่อยู่ลูกค้า')
    send_bill_status = models.CharField(max_length=50, verbose_name='สถานะการส่งบิล')
    collateral_id = models.IntegerField(verbose_name='รหัสหลักประกัน')
    collateral_type = models.CharField(max_length=255, verbose_name='ประเภทหลักประกัน')
    chassis_no = models.CharField(max_length=255, verbose_name='เลขตัวถัง')
    engine_no = models.CharField(max_length=255, verbose_name='เลขเครื่องยนต์')
    reg_no = models.CharField(max_length=255, verbose_name='เลขทะเบียน')
    province_name = models.CharField(max_length=255, verbose_name='ชื่อจังหวัด')
    collateral_slug = models.SlugField(unique=True, verbose_name='Slug หลักประกัน')
    sum_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ยอดชำระทั้งหมด')
    sum_revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='รายได้รวม')
    sum_tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ภาษีรวม')
    CONT_STATUS_SLIP = [
        ("A", "ACTIVE"),
        ("F", "NONACTIVE"),
    ]
    status = models.CharField(max_length=50,choices=CONT_STATUS_SLIP ,verbose_name='สถานะ')
    status_name = models.CharField(max_length=255, verbose_name='ชื่อสถานะ')
    CONT_STATUS_CHOICES = [
        ("V", "หนี้สูญทางบัญชี"),
        ("C", "ปิดบัญชี"),
        ("T", "ปิดปรับ TDR"),
        ("A", "เป็นลูกหนี้"),
    ]
    cont_status = models.CharField(
        max_length=50, choices=CONT_STATUS_CHOICES, verbose_name='สถานะสัญญา')
    cont_status_name = models.CharField(max_length=255, verbose_name='ชื่อสถานะสัญญา')
    cont_status_date = models.DateField(verbose_name='วันที่สถานะสัญญา')
    created_at = models.DateTimeField(verbose_name='สร้างเมื่อ')
    updated_at = models.DateTimeField(verbose_name='อัปเดตเมื่อ')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    active_post_gl = models.BooleanField(default=False, verbose_name='โพสต์ GL ที่ใช้งานอยู่')
    cancel_post_gl = models.BooleanField(default=False, verbose_name='ยกเลิกโพสต์ GL')
    principal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='เงินต้น')

    # new model here of LineOA_contract function
    installment_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ยอดผ่อนชำระแล้ว')
    principal_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='เงินต้นที่ชำระแล้ว')
    sum_principal_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ยอดเงินทั้งหมดที่ชำระแล้ว')
    interest_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ดอกเบี้ยที่ชำระแล้ว')
    last_payment_date = models.DateField(verbose_name='วันที่ชำระเงินล่าสุด')
    next_due_date = models.DateField(verbose_name='วันครบกำหนดถัดไป')
    over_due_period = models.IntegerField(verbose_name='จำนวนงวดค้างชำระ')
    over_due_from = models.DateField(verbose_name='ค้างชำระตั้งแต่งวดที่ $ ')
    over_due_to = models.DateField(verbose_name='ค้างชำระถึงงวดที่ $')
    dpd = models.IntegerField(verbose_name='จำนวนวันที่ค้างชำระ')
    installment_over_due = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ยอดค้างชำระ')
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ยอดเงินต้นคงเหลือ')
    interest_over_due = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ดอกเบี้ยค้างชำระ')
    close_acc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ยอดปิดบัญชี')
    collection_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ค่าทวงถามหนี้ทั้งหมด')

    # ---------------------------------------------------------------------------------------------------

    class Meta:
        db_table = 'LineOA_ViewCustomer'
        # ordering = ['card_no']
        managed = False

    #-------------------------------------format date-------------------------------------
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

        return '<span style="color: red;">ไม่มีข้อมูลวันที่</span>'
    
    # วันที่ชำระล่าสุด
    def lastpaydate(self):
        return self.format_date(self.last_payment_date)
    
    def cont_statusdue(self):
        return self.format_date(self.cont_status_date)
    
    def startdate(self):
        return self.format_date(self.cont_date)
    
    def nextdate(self):
        return self.format_date(self.next_due_date)
    
    # จำนวนวันค้างชำระ
    def overduedate(self):
        return self.format_date(self.dpd)
    
    
    
    #---------------------------------------------------------------------------------------------------------------------
    #format money

    def format_money(self, money):

        if money is not None:
            return f"{money:,.2f}"  # ใส่, กับ ทศนิยม 2 ตำแหน่ง
        return "ไม่มียอดคงเหลือ"
    
    # เงินต้นที่จ่ายแล้วล่าสุด
    def cashspended(self) :
        return self.format_money(self.principal_paid)
    
    # ดอกเบี้ยที่จ่ายแล้ว
    def fee_spended(self) :
        return self.format_money(self.interest_paid)
    
    # def lastdate(self):
    #     return self.format_date(self)
    
    # เงินต้นคงเหลือทั้งหมด
    def moneypricipal_remain(self) :
        return self.format_money(self.principal_amount)
    
    #ยอดชำระทั้งหมด
    def moneytotal(self) :
        return self.format_money(self.sum_principal_paid)
    
    # เงินต้นที่ต้องชำระ
    # def moneyfirst(self) :
    #     return self.format_money(self.)
    
    # ยอดเงินต้นค้างชำระ
    def moneyfirst_over_due(self) :
        return self.format_money(self.installment_over_due)
    
    # ยอดปิดบัญชี
    def moneyfirst_last_period(self) :
        return self.format_money(self.close_acc)
    
    #ดอกเบี้ย format
    def money_r_finish(self) :
        return self.format_money(self.interest_paid)
    
    # ดอกเบี้ยค้างชำระ
    def money_r_inprocess(self) :
        return self.format_money(self.interest_over_due)
    
    # ยอดปิดบัญชี
    def money_closeacc(self) :
        return self.format_money(self.close_acc)
    

    # ยอดเงินต้นเกินกำหนดชำระ
    # def prici_overdue(self) :
    #     return self.format_money(self.)

def loan_penalty(contract_id, ar_date, cont_type , contract_detail_id=0 ):
    try:
        contract_info = LineOA_contract.objects.get(id=contract_id, cont_type=cont_type)
    except LineOA_contract.DoesNotExist:
        contract_info = None
    if contract_info:
        if contract_detail_id > 0:
            if contract_info.sequence_method == 'H':
                obj_loan_penalty = Loan_Penalty_BOT.objects.raw('''SELECT * FROM Loan_Penalty_BOT(%s, %s, %s) WHERE payment > 0''',
                                                                [contract_id, ar_date, contract_detail_id])
            else:
                obj_loan_penalty = Loan_Penalty_BOT.objects.raw('''SELECT * FROM Loan_Penalty(%s, %s, %s) WHERE payment > 0''',
                                                                [contract_id, ar_date, contract_detail_id])
        else:
            if contract_info.sequence_method == 'H':
                obj_loan_penalty = Loan_Penalty_BOT.objects.raw('''SELECT * FROM Loan_Penalty_BOT(%s, %s, default) WHERE payment > 0''',
                                                                [contract_id, ar_date])
            else:
                obj_loan_penalty = Loan_Penalty_BOT.objects.raw('''SELECT * FROM Loan_Penalty(%s, %s, default) WHERE payment > 0''',
                                                                [contract_id, ar_date])
    else:
        obj_loan_penalty = None
    return obj_loan_penalty
