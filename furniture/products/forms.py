from django import forms
from products.models import OrderProduct


class OrderProductForm(forms.ModelForm):

    # products = forms.CharField(widget=forms.HiddenInput())

    # def save(self, commit=True):
    #     order = super().save(commit=False)
    #     if commit:
    #         order.save()

    #     # Преобразуем строку JSON из формы в список и сохраняем в поле
    #     product_ids = self.cleaned_data['products'].split(',')
    #     order.set_products(product_ids)
    #     order.save()

    #     return order
    class Meta:
        model = OrderProduct
        fields = ['products','name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7...'}),
            'products': forms.MultipleHiddenInput()
        }
    
