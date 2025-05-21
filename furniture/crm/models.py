from django.db import models

class TypeOperation(models.Model):
    name = models.CharField(verbose_name="Наименование",max_length=50,unique=True)
    
    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операции"

    def __str__(self):
        return self.name

class ElementProduct(models.Model):
    name = models.CharField(verbose_name="Наименование",max_length=100)
    price = models.DecimalField(verbose_name="Стоимость",max_digits=10,decimal_places=2)
    count = models.PositiveIntegerField(verbose_name="Количество")
    type_operation = models.ForeignKey(TypeOperation,on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    
    class Meta:
        verbose_name = "Товар CRM"
        verbose_name_plural = "Товары CRM"

    def __str__(self):
        return self.name