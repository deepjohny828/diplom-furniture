from django.contrib import admin
from products.models import Product, Category, OrderProduct


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    max_num = 0
    can_delete = False
    show_change_link = True
    fields = ("name", "product_price", "available")
    readonly_fields = ("name", "product_price", "available")
    ordering = ["-available"]

    def product_price(self, obj):
        return f"{obj.price} ₽"

    product_price.short_description = "Цена"


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price_with_discount_formatted", "discount_formatted")

    def price_with_discount_formatted(self, obj):
        return f"{obj.price_with_discount()} ₽"

    price_with_discount_formatted.short_description = "Цена со скидкой"

    def discount_formatted(self, obj):
        return f"{obj.discount} %"

    discount_formatted.short_description = "Скидка"
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ("name", "product_count")
    prepopulated_fields = {"slug": ("name",)}

    def product_count(self, obj):
        return obj.product_set.count()

    product_count.short_description = "Кол-во товаров"
