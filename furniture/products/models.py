from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
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

class Feedback(models.Model):
    email = models.EmailField(verbose_name="Email")
    
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = "Почта пользователя"
        verbose_name_plural = "Почты пользователей"

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
        verbose_name_plural = "Материалы"


class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider/', verbose_name="Изображение для слайдера")
    alt_text = models.CharField(max_length=255, verbose_name="Текст для alt", blank=True)
    link = models.URLField(blank=True, null=True, verbose_name="Ссылка для слайда")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения", help_text="Меньшие значения отображаются раньше")

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение слайдера'
        verbose_name_plural = 'Изображения слайдера'

    def __str__(self):
        return f"Слайд {self.id}"


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
        db_index=True,

    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    sale_price = models.DecimalField(
        verbose_name="Стоимость продажи*",
        decimal_places=2,
        max_digits=10,
        db_index=True,
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
        blank=True
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
        blank=True
    )
    available = models.BooleanField("Активен в каталоге", default=True)
    is_sold = models.BooleanField("Продан", default=False)
    date_sold = models.DateTimeField("Дата продажи", blank=True, null=True)


    is_seasonal = models.BooleanField(
        verbose_name="Сезонный товар",
        default=False,
        help_text="Отобразит бейджик 'Сезонный товар' у товара"
    )
    is_bestseller = models.BooleanField(
        verbose_name="Хит продаж",
        default=False,
        help_text="Отобразит бейджик 'Хит продаж' у товара"
    )
    is_new = models.BooleanField(
        verbose_name="Новинка",
        default=True,
        help_text="Отобразит бейджик 'Новинка' у товара"
    )

    views = models.PositiveIntegerField(
        verbose_name="Просмотры",
        default=0,
        editable=False,
        db_index=True,
    )
    compare_count = models.PositiveIntegerField(
        verbose_name="Количество сравнений",
        default=0,
        editable=False
    )


    @property
    def price_with_discount(self):
        return round((self.sale_price - (self.sale_price * self.discount) / 100), 2)


    def clean(self):
        super().clean()
        selected_fields = [self.is_seasonal, self.is_bestseller, self.is_new]
        true_count = sum(selected_fields)
        if true_count > 1:
            raise ValidationError("Можно выбрать только один статус (Сезонный, Хит продаж или Новинка)!")

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
        if self.sale_price < self.price:
            raise ValueError("Цена продажи не может быть ниже закупочной цены")
        if self.is_sold:
            self.available = False
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["is_sold"]
        indexes = [
            models.Index(fields=["name", "category"]),
            models.Index(fields=["price", "sale_price"]),
            models.Index(fields=["available", "is_sold"]),
        ]

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
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    created_at = models.DateTimeField(verbose_name="Дата заявки", auto_now_add=True)
    active = models.BooleanField(
        verbose_name="Заявка активна", default=1
    )
    auto_complete = models.BooleanField(
        verbose_name="Проставить все позиции на 'продано'?", default=0
    )
    products = models.ManyToManyField("Product", verbose_name="Товары",through="OrderProductItem")

    def save(self, *args, **kwargs):
        if self.auto_complete:
            for item in self.orderproductitem_set.all():
                product = item.product
                product.is_sold = True
                product.available = False
                product.save()
            self.active = False  # Изменяем поле
            self.auto_complete = False
        super().save(*args, **kwargs)  # Сохраняем все изменения

    def __str__(self):
        return f"От: {self.name}"
    class Meta:
        verbose_name = "Заявка на товар"
        verbose_name_plural = "Заявки на товар"
        ordering = ["active", "created_at"]

        
class OrderProductItem(models.Model):
    order = models.ForeignKey(OrderProduct,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order.id} - {self.product.name}" 
    

