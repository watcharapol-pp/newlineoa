from django import forms

class SearchForm(forms.Form):
    card_no = forms.CharField(
        label="กรอกเลขบัตรประชาชน",
        max_length=40,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'ใส่เลขบัตรประชาชน',
            'style': 'margin-top: 10px; width: 300px; height: 40px; font-size: 18px;'
        })
        
    )
