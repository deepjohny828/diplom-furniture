from django import forms
from products.models import OrderProduct


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['product','name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7...'}),
            'product': forms.HiddenInput()
        }
    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if len(name) < 2:
    #         raise forms.ValidationError("Имя слишком короткое")
    #     return name
        # model = OrderProduct
        # fields = ["name", "email", "phone"]
        # widgets = {
        #     "phone": forms.TextInput(attrs={"placeholder": "+7 (XXX)XXX-XX-XX"}),
        #     "name": forms.TextInput(attrs={"placeholder": "Иван Иванов"}),
        #     "email": forms.TextInput(attrs={"placeholder": "ivanivanov@mail.ru"}),
        # }
