from django import forms
from crm.models import ElementProduct,TypeOperation

class ElementProductForm(forms.ModelForm):
    type_operation = forms.ModelChoiceField(
        queryset=TypeOperation.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Тип операции'
    )
    class Meta:
        model = ElementProduct
        fields = ["price","name","count","type_operation"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
            # Как заменить type на выпадающий список
        }