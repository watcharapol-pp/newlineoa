from django import forms

class SearchForm(forms.Form):
    card_no = forms.CharField(
        label="กรอกบัตรประชาชน",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'ใส่เลขบัตรประชาชน',
            'style': 'margin-top: 10px; height: 40px; font-size: 18px;'
        })
        
    )
    def clean_card_no(self):
        card_no = self.cleaned_data.get('card_no')

        # ตรวจสอบว่าต้องเป็นตัวเลขเท่านั้น
        if not card_no.isdigit():
            raise forms.ValidationError("กรุณากรอกเฉพาะตัวเลขเท่านั้น")

        # ตรวจสอบว่าต้องมี 13 ตัวพอดี
        if len(card_no) != 13:
            raise forms.ValidationError("กรุณากรอกเลขบัตรให้ครบ 13 ตัว")

        return card_no
