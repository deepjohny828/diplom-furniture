from django import forms
from products.models import OrderProduct

class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['products','name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7...'}),
            'products': forms.MultipleHiddenInput()
        }
    
