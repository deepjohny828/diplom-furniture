from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import localtime
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(
        verbose_name="Название категории*", unique=True, max_length=50
    )
    slug = models.SlugField(unique=True, verbose_name="Метка (slug)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(verbose_name="Название бренда*", max_length=100, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

class Color(models.Model):
    name = models.CharField("Цвет*", max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class Material(models.Model):
    name = models.CharField("Материал*", max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Метериалы"


def generate_article_number(pk):
    return f"PRD-{str(pk).zfill(5)}"


class Product(models.Model):
    name = models.CharField(
        verbose_name="Название*",
        db_index=True,
        max_length=150,
    )
    price = models.DecimalField(
        verbose_name="Стоимость закупки*",
        decimal_places=2,
        max_digits=10,
        db_index=True
    )
    sale_price = models.DecimalField(
        verbose_name="Стоимость продажи*",
        decimal_places=2,
        max_digits=10,
        db_index=True
    )
    slug = models.SlugField(unique=True, verbose_name="Метка (slug)")
    category = models.ForeignKey(
        Category,
        verbose_name="Категория*",
        on_delete=models.CASCADE,
        db_index=True,
    )
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    image = models.ImageField(verbose_name="Изображение*", upload_to="%Y/%m/%d")
    description = models.TextField(verbose_name="Описание", blank=True, default="")
    discount = models.PositiveIntegerField(
        verbose_name="Размер скидки",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(99)],
    )
    article_number = models.CharField(
        verbose_name="Артикул",
        unique=True,
        max_length=20,
        blank=True,
        help_text="Будет автоматически сгенерирован после сохранения!",
    )
    brand = models.ForeignKey(
        to=Brand, verbose_name="Бренд", on_delete=models.SET_NULL, null=True, blank=True
    )
    width = models.PositiveIntegerField(
        "Ширина (мм)*", help_text="Укажите в миллиметрах"
    )
    height = models.PositiveIntegerField(
        "Высота (мм)*", help_text="Укажите в миллиметрах"
    )
    depth = models.PositiveIntegerField(
        "Глубина (мм)*", help_text="Укажите в миллиметрах"
    )
    color = models.ForeignKey(
        Color, verbose_name="Цвет", on_delete=models.SET_NULL, null=True, blank=True
    )

    material = models.ForeignKey(
        Material,
        verbose_name="Материал",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    # in_stock = models.PositiveIntegerField("Остаток на складе", default=0)
    available = models.BooleanField("Активен в каталоге", default=True)
    is_sold = models.BooleanField("Продан", default=False)
    # date_purchased = models.DateTimeField("Дата закупки", blank=True, null=True)
    date_sold = models.DateTimeField("Дата продажи", blank=True, null=True)
    
    @property
    def price_with_discount(self):
        return round((self.sale_price - (self.sale_price * self.discount) / 100), 2)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if not self.article_number:
            self.article_number = generate_article_number(self.pk)
            super().save(update_fields=["article_number"])
        if is_new:
            Purchase.objects.create(
                product=self, purchase_date=timezone.now(), purchase_price=self.price
            )
        if self.is_sold:
            self.date_sold = timezone.now()
            self.available = False
        if not self.is_sold:
            self.date_sold = None


        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["is_sold"]

    def __str__(self):
        return self.name


class Purchase(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    purchase_price = models.DecimalField(
        verbose_name="Стоимость закупки",
        decimal_places=2,
        max_digits=10,
        db_index=True,
    )
    purchase_date = models.DateTimeField(auto_now_add=True)
    type_operation = models.CharField("Тип операции", max_length=10, default="Закупки",editable=False)
    def __str__(self):
        local_created = localtime(self.purchase_date)
        return f"{self.product.name} | взято за {self.purchase_price} руб. |  дата: {local_created.strftime('%d-%m-%Y %H:%M:%S')}"
    class Meta:
        verbose_name = "Закупку"
        verbose_name_plural = "Закупки"

class OrderProduct(models.Model):
    name = models.CharField(verbose_name="Имя клиента", max_length=100)
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(verbose_name="Номер телефона", max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    created_at = models.DateTimeField(verbose_name="Дата заявки", auto_now_add=True)
    active = models.BooleanField(
        verbose_name="Заявка активна", default=1, max_length=20
    )
    def save(self, *args, **kwargs):
        if not self.active:
            self.product.is_sold = True
            self.product.save()
        elif self.active:
            self.product.is_sold = False
            self.product.save()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Заявка на товар"
        verbose_name_plural = "Заявки на товар"
        ordering = ["active", "created_at"]

        
