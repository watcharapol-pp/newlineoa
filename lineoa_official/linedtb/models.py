from django.db import models
from datetime import datetime

class ContractInfoManager(models.Manager):
    # def with_payments(self):
    #     return self.prefetch_related("contractpaymentdetail_set")
    # def get_related_contracts(self, cont_no):
    #     return self.filter(cont_no=cont_no)

    def get_related_contracts(self, cont_no):
        return self.prefetch_related("payments").filter(cont_no=cont_no)
    

class ContractInfo(models.Model):
    objects = ContractInfoManager()

    # id = models.AutoField(verbose_name='id ประจำรายการ')
    contract_detail_id = models.IntegerField(verbose_name='contract_id')
    branch_id = models.IntegerField(verbose_name='branch_id')
    branch_code = models.CharField(max_length=255, verbose_name='รหัสสำนักงาน')
    branch_name = models.CharField(max_length=255, verbose_name='ประเภทสำนักงาน')
    cont_type = models.CharField(max_length=255, verbose_name='ประเภทสัญญา')
    cont_type_name = models.CharField(max_length=255, verbose_name='ชื่อประเภทสัญญา')
    cont_no = models.CharField(max_length=50, unique=True, verbose_name='เลขที่สัญญา')
    cont_date = models.DateField(verbose_name='วันที่เริ่มสัญญา')
    actual_date = models.DateField(verbose_name='วันที่จริง')
    cont_group_id = models.IntegerField(verbose_name='รหัสกลุ่มสัญญา')
    cont_group_code = models.CharField(max_length=50, verbose_name='รหัสกลุ่ม')
    cont_group_name = models.CharField(max_length=255, verbose_name='ชื่อกลุ่ม')
    sequence_method = models.CharField(max_length=255, verbose_name='วิธีการเรียงลำดับ')
    ar_type = models.CharField(max_length=255, verbose_name='ประเภท AR')
    ar_type_name = models.CharField(max_length=255, verbose_name='ชื่อประเภท AR')
    payment_terms = models.CharField(max_length=255, verbose_name='จำนวนงวดที่ชำระแล้ว')
    payment_terms_name = models.CharField(max_length=255, verbose_name='ชื่อเงื่อนไขการชำระเงิน')
    customer_id = models.IntegerField(verbose_name='รหัสลูกค้า')
    customer_name = models.CharField(max_length=300, verbose_name='ชื่อลูกค้า')
    card_no = models.CharField(max_length=20, unique=True, verbose_name='เลขบัตรประชาชน')
    mobile = models.CharField(max_length=15, verbose_name='เบอร์โทรศัพท์')
    customer_slug = models.SlugField(unique=True, verbose_name='Slug ลูกค้า')
    customer_address_id = models.IntegerField(verbose_name='รหัสที่อยู่ลูกค้า')
    send_bill_status = models.CharField(max_length=50, verbose_name='สถานะการส่งบิล')
    collateral_id = models.IntegerField(verbose_name='รหัสหลักประกัน')
    collateral_type = models.CharField(max_length=255, verbose_name='ประเภทหลักประกัน')
    collateral_type_name = models.CharField(max_length=255, verbose_name='ชื่อประเภทหลักประกัน')
    chassis_no = models.CharField(max_length=255, verbose_name='เลขตัวถัง')
    engine_no = models.CharField(max_length=255, verbose_name='เลขเครื่องยนต์')
    reg_no = models.CharField(max_length=255, verbose_name='เลขทะเบียน')
    province_name = models.CharField(max_length=255, verbose_name='ชื่อจังหวัด')
    collateral_slug = models.SlugField(unique=True, verbose_name='Slug หลักประกัน')
    sum_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ยอดชำระทั้งหมด')
    sum_revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='รายได้รวม')
    sum_tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ภาษีรวม')
    status = models.CharField(max_length=50, verbose_name='สถานะ')
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
    sum_principal_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ยอดเงินต้นที่ชำระแล้ว')

    class Meta:
        db_table = 'View_Contract'
        # ordering = ['card_no']
        managed = False

    
    # Function 1: ตรวจสอบสถานะ
    def is_active_status(self):
        """ ตรวจสอบว่าสถานะเป็น Active หรือไม่ """
        return self.status.lower() == 'active'
    
    # Function 2: ดึงชื่อเต็ม
    def get_full_name(self):
        """ ดึงชื่อเต็มของบุคคล """
        return self.customer_name
    
    def get_nam_car(self):
        """ ดึงทะเบียนรถ """
        return self.reg_no
    
    # Function 4: สรุปข้อมูลแบบง่าย
    def summary(self):
        """ ดึงข้อมูลสำคัญของผู้ใช้งาน """
        return f"Name: {self.customer_name}, Status: {self.status}"
    

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

    
    # def format_datee(self, date_value):
    #     date = str(date_value)
    #     datestr = None
    #     if len(date) == 7 :
    #         datestr = str('0' + date)
    #     elif len(date) == 8 :      
    #         datestr = str(date)

    #     if len(datestr) == 8:  
    #         try:
    #             due_obj = datetime.strptime(datestr, '%Y%m%d')  
    #             return due_obj.strftime('%d/%m/%Y')  
    #         except ValueError:
    #             return "1"  
    #     else:
    #         return "ไม่มีข้อมูลวันที่"  
        

    def day_due(self):
        return self.format_date(self.cont_date)
    

    # def nextdate(self):
    #     return self.format_date(self.)
    
    # def lasteddate(self):
    #     return self.format_date(self.actual_date)
    
    def cont_statusdue(self):
        return self.format_date(self.cont_status_date)
    
    def format_money(self, money):

        if money is not None:
            return f"{money:,.2f}"  # ใส่, กับ ทศนิยม 2 ตำแหน่ง
        return "ไม่มียอดคงเหลือ"
    
    # def moneyfm(self) :
    #     return self.format_money(self.)
    

class Contractpaymentdetail(models.Model):

    branch_id = models.IntegerField(verbose_name='รหัสสำนักงาน')
    contract_detail_id = models.IntegerField(verbose_name='contractdetail')
    contract_id = models.IntegerField(verbose_name='contract_idd')

    # peyment
    payment_id = models.IntegerField(verbose_name='ID ใบเสร็จ')
    payment_no = models.CharField(max_length=255, verbose_name='รหัสใบเสร็จ')
    payment_date = models.DateField(verbose_name='วันที่ชำระเงิน')

    #--------------------------------------------------------------------
    payfor_id = models.IntegerField(verbose_name='รหัสรูปแบบการจ่าย')
    payfor_code = models.IntegerField(verbose_name='เลขกำกับรูปแบบการจ่าย')
    payfor_type = models.CharField(max_length=255, verbose_name='ชนิดการจ่าย')
    payfor_name = models.CharField(max_length=255, verbose_name='ชื่อของการจ่าย')
    cont_type = models.CharField(max_length=255, verbose_name='ประเภทสัญญา')

    payment = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='จำนวนเงินที่จ่าย')
    net_payment = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='รายจ่ายสุทธิ')
    vat_payment = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ค่า vat แยก')
    discount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ส่วนลด')
    total_payment = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ยอดชำระทั้งหมด')
    principal_paid = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='เงินต้นที่ชำระแล้ว')
    principal_over_due = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='เงินต้นค้างชำระ')
    principal_due = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='เงินต้นที่ถึงกำหนดชำระ')
    principal_remaining = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='เงินต้นคงเหลือ')
    days_paid = models.IntegerField(verbose_name='จำนวนวันที่ชำระ')
    interest_paid = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ดอกเบี้ยที่ชำระแล้ว')
    interest_over_due = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ดอกเบี้ยค้างชำระ')
    interest_due = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ดอกเบี้ยที่ถึงกำหนดชำระ')
    interest_remaining = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ดอกเบี้ยคงเหลือที่ต้องจ่าย')
    fee_paid = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ค่าธรรมเนียมที่ชำระแล้ว')
    principal_balance = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ยอดเงินต้นคงเหลือ')
    penalty = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ค่าปรับ')
    first_period = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ลำดับงวดแรกที่ชำระ')
    last_period = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='ลำดับงวดสุดท้ายที่ชำระ')
    status = models.CharField(max_length=50, verbose_name='สถานะการชำระ')
    status_name = models.CharField(max_length=50, verbose_name='ชื่อสถานะการชำระ')
    next_due_date = models.DateField(verbose_name='วันครบกำหนดถัดไป')
    

    class Meta:
        db_table = 'LineOA_ViewPaymentDetail'
        managed = False


    # def __str__(self):
    #     return str(self.id)

    # Function 1: ตรวจสอบสถานะ
    @property
    def is_active_status(self):
        """ ตรวจสอบว่าสถานะเป็น Active หรือไม่ """
        return self.status.lower() == 'active'
    
    
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
    
    # def format_date(self, date_value):
    #     if date_value:
    #         date_str = str(date_value)  
            
    #         if len(date_str) == 8:  
    #             try:
    #                 date_obj = datetime.strptime(date_str, '%Y-%m-%d')  
    #                 return date_obj.strftime('%d/%m/%Y')  
    #             except ValueError:
    #                 return "1"  
    #         else:
    #             return "2"  
    #     return "ไม่มีข้อมูลวันที่"
    
    # def format_datee(self, date_value):
    #     date = str(date_value)
    #     datestr = None
    #     if len(date) == 7 :
    #         datestr = str('0' + date)
    #     elif len(date) == 8 :      
    #         datestr = str(date)

    #     if len(datestr) == 8:  
    #         try:
    #             due_obj = datetime.strptime(datestr, '%Y%m%d')  
    #             return due_obj.strftime('%d/%m/%Y')  
    #         except ValueError:
    #             return "1"  
    #     else:
    #         return "ไม่มีข้อมูลวันที่"  

        # return "ไม่มีข้อมูลวันที่"

    # def day_due(self):
    #     return self.format_date(self.CURRDUE)
    
    @property
    def nextdate(self):
        return self.format_date(self.next_due_date)
    @property
    def paydate(self):
        return self.format_date(self.payment_date)
    
    # def lastdate(self):
    #     return self.format_date(self)
    def format_money(self, money):

        if money is not None:
            return f"{money:,.2f}"  # ใส่, กับ ทศนิยม 2 ตำแหน่ง
        return "ไม่มียอดคงเหลือ"
    
    # เงินต้นคงเหลือ
    @property
    def moneypricipal_remain(self) :
        return self.format_money(self.principal_remaining)
    
    # ยอดที่จ่ายมา
    @property
    def paymentspended(self) :
        return self.format_money(self.payment)
    
    #ยอดชำระทั้งหมด
    @property
    def moneytotal(self) :
        return self.format_money(self.total_payment)
    
    # เงินต้นที่ต้องชำระ
    @property
    def moneyfirst(self) :
        return self.format_money(self.principal_due)
    
    # เงินต้นที่ชำระมาแล้ว
    @property
    def moneyfirst_paid(self) :
        return self.format_money(self.principal_paid)
    

    @property
    def moneyfirst_over_due(self) :
        return self.format_money(self.principal_over_due)
    
    # ยอดปิดบัญชี
    @property
    def moneyfirst_last_period(self) :
        return self.format_money(self.last_period)
    
    #ดอกเบี้ย format
    @property
    def money_r_finish(self) :
        return self.format_money(self.interest_paid)
    
    @property
    def money_r_inprocess(self) :
        return self.format_money(self.interest_due)
    

    # ยอดเงินต้นเกินกำหนดชำระ
    @property
    def prici_overdue(self) :
        return self.format_money(self.principal_over_due)
    
    # ส่วนลด
    @property
    def discount_pay(self) :
        return self.format_money(self.discount)
    
    # 
    # def periodoverdue(self) :
    #     return self.format_money(self.)
    

    
    
        # return f"{self.TOTALAMOUNTDUE:,.2f}"
    

    

    



    # def day_due(self):
    #     print(self.CURRDUE)
    #     # print(self.CURRDUE)
    #     if self.CURRDUE:
    #         # แปลง Integer เป็น string ก่อน
    #         date_str = str(self.CURRDUE)

    #         if len(date_str) == 7 or len(date_str) == 8:
    #             try:
    #                 # แปลงจาก 'YYYYMMDD' เป็น datetime object
    #                 date_obj = datetime.strptime(date_str, '%Y%d%m')

    #                 return date_obj.strftime('%d/%m/%Y')
    #             except ValueError:
    #                 return "1"
    #         else:
    #             return "2"
    #     return "ไม่มีข้อมูลวันที่"
    
    # def nextdate(self):
    #     print(self.NEXTSCHEDULEDATEPAYMENT)
    #     if self.NEXTSCHEDULEDATEPAYMENT:
    #         # แปลง Integer เป็น string ก่อน
    #         nexdate = str(self.NEXTSCHEDULEDATEPAYMENT)

    #         if len(nexdate) == 7 or len(nexdate) == 8:
    #             try:
    #                 # แปลงจาก 'YYYYMMDD' เป็น datetime object
    #                 dateobj = datetime.strptime(nexdate, '%Y%d%m')

    #                 return dateobj.strftime('%d/%m/%Y')
    #             except ValueError:
    #                 return "1"
    #         else:
    #             return "2"
    #     return "ไม่มีข้อมูลวันที่"



    # def contract_pm_dt(self):
    #     Contractpaymentdetail.objects.filter(contract_detail_id = self.contract_detail_id)
