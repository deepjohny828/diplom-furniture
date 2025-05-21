from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError

def str_to_decimal(value: str) -> Decimal:
    try:
        cleaned_value = value.strip().replace(',', '.')
        return Decimal(cleaned_value)
    except (InvalidOperation, TypeError, ValueError):
        raise ValidationError(f"Невозможно преобразовать '{value}' в десятичное число")