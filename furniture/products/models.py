from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import localtime

class Category(models.Model):
    name = models.CharField(
        verbose_name="Название категории", unique=True, max_length=50
    )
    slug = models.SlugField(unique=True, verbose_name="Метка (slug)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        verbose_name="Название",
        db_index=True,
        max_length=150,
    )
    price = models.DecimalField(
        verbose_name="Стоимость",
        decimal_places=2,
        max_digits=10,
        db_index=True,
    )
    slug = models.SlugField(unique=True, verbose_name="Метка (slug)")
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        db_index=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    available = models.BooleanField(
        verbose_name="Доступно", default=True, db_index=True
    )
    image = models.ImageField(verbose_name="Изображение", upload_to="%Y/%m/%d")
    description = models.TextField(verbose_name="Описание", blank=True, default="")
    discount = models.PositiveIntegerField(
        verbose_name="Размер скидки",
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(99)],
    )

    def price_with_discount(self):
        return round((self.price - (self.price * self.discount) / 100), 2)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class OrderProduct(models.Model):
    name = models.CharField(verbose_name="Имя клиента", max_length=100)
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(verbose_name="Номер телефона", max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    created_at = models.DateTimeField(verbose_name="Дата заявки", auto_now_add=True)
    active = models.BooleanField(verbose_name="Заявка активна", default=1,max_length=20)

    class Meta:
        verbose_name = "Заявка на товар"
        verbose_name_plural = "Заявки на товар"
        ordering = ["active", "created_at"]

    def __str__(self):
        local_created = localtime(self.created_at)
        return f"Заявка на {self.product.name} от {local_created.strftime('%d-%m-%Y %H:%M:%S')}"
