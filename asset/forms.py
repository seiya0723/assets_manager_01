from django import forms
from .models import Balance

class BalanceForm(forms.ModelForm):
    class Meta:
        model     = Balance
        fields   = [ "category","title","comment","income","spending","pay_dt"]
