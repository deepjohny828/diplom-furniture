from django import forms
from .models import Feedback, OrderProduct
from django.utils.safestring import mark_safe 

class OrderProductForm(forms.ModelForm):
    # Добавляем поле для согласия (не привязано к модели)
    consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'consent-checkbox',
            'style': 'margin-right: 8px;'  # Отступ между чекбоксом и текстом
        }),
        label='',
        error_messages={
            'required': 'Необходимо дать согласие на обработку данных'
        }   
    )

    class Meta:
        model = OrderProduct
        fields = ['products', 'name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7...'}),
            'products': forms.MultipleHiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем HTML-разметку к label
        self.fields['consent'].help_text = mark_safe(
            '<span style="margin-left: 5px;">Я согласен на обработку'
            '<a href="/privacy_policy/" target="_blank" style="color: #0066cc;"> персональных данных</a></span>'
        )

class FeedbackForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='',
        error_messages={
            'required': 'Необходимо дать согласие на обработку данных'
        }
    )
    
    class Meta:
        model = Feedback
        fields = ['email', 'consent']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ваш email',
                'class': 'form-control email-input',
                'style': 'max-width: 300px;'  # Ограничение ширины поля
            }),
        }
        labels = {
            'email': '',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['consent'].help_text = mark_safe(
            '<span class="consent-text">Я согласен на <a href="/privacy_policy/" class="privacy-link">обработку персональных данных</a></span>'
        )