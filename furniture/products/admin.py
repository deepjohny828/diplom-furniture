from django.contrib import admin
from products.models import (
    Product,
    Category,
    OrderProduct,
    Material,
    Color,
    Purchase,
    OrderProductItem,
    SliderImage
)
from django.utils.timezone import localtime

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.admin import DateFieldListFilter
from django.urls import reverse
from django.utils.html import format_html, format_html_join
import json
from django.utils.safestring import mark_safe

@admin.register(SliderImage)
class SliderImage(admin.ModelAdmin):
    list_display = ['id', 'image', 'order', 'link', 'alt_text']
    search_fields = ['alt_text', 'link']
    list_filter = ['order']
    ordering = ['order']

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_link",
        "action_flag_verbose",
        "pretty_change_message",
    ]
    list_filter = [
        "action_flag",
        "content_type",
        "user",
        ("action_time", DateFieldListFilter),
    ]
    search_fields = ["object_repr", "user__username", "change_message"]
    ordering = ("-action_time",)
    readonly_fields = [f.name for f in LogEntry._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def action_flag_verbose(self, obj):
        return {
            ADDITION: "Создание",
            CHANGE: "Изменение",
            DELETION: "Удаление",
        }.get(obj.action_flag, "Неизвестно")

    action_flag_verbose.short_description = "Действие"
    action_flag_verbose.admin_order_field = "action_flag"

    def short_change_message(self, obj):
        msg = obj.change_message
        return (msg[:75] + "...") if len(msg) > 75 else msg

    short_change_message.short_description = "Описание изменений"

    def object_link(self, obj):
        try:
            url = reverse(
                f"admin:{obj.content_type.app_label}_{obj.content_type.model}_change",
                args=[obj.object_id],
            )
            return format_html('<a href="{}">{}</a>', url, obj.object_repr)
        except Exception:
            return obj.object_repr

    object_link.short_description = "Объект"
    object_link.admin_order_field = "object_repr"

    def pretty_change_message(self, obj):
        try:
            changes = json.loads(obj.change_message)
        except Exception:
            return obj.change_message  # если не JSON, вернуть как есть

        messages = []
        for change in changes:
            if "changed" in change:
                fields = change["changed"].get("fields", [])
                messages.append(f"Изменены поля: {', '.join(fields)}")
            elif "added" in change:
                fields = change["added"].get("fields", [])
                messages.append(f"Добавлены поля: {', '.join(fields)}")
            elif "removed" in change:
                fields = change["removed"].get("fields", [])
                messages.append(f"Удалены поля: {', '.join(fields)}")
            else:
                messages.append(str(change))

        return format_html("<br>".join(messages))

    pretty_change_message.short_description = "Описание изменений"


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    max_num = 0
    can_delete = False
    show_change_link = True
    fields = ("name", "product_price", "available", "is_sold")
    readonly_fields = ("name", "product_price", "available", "is_sold")
    ordering = ["is_sold", "available"]

    def product_price(self, obj):
        return f"{obj.price} ₽"

    product_price.short_description = "Цена"


class OrderProductItemInline(admin.TabularInline):
    model = OrderProductItem
    extra = 0
    max_num = 0
    can_delete = False
    show_change_link = True

    # Методы – только в readonly_fields
    readonly_fields = ("product_link", "product_price", "product_available", "product_is_sold")
    # А в fields – те же названия
    fields = ("product_link", "product_price", "product_available", "product_is_sold")

    def product_link(self, obj):
        url = reverse('admin:products_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = "Товар"

    def product_price(self, obj):
        return f"{obj.product.price_with_discount} ₽"
    product_price.short_description = "Цена со скидкой"

    def product_available(self, obj):
        icon = "✅" if obj.product.available else "❌"
        return format_html(icon)
    product_available.short_description = "В наличии"

    def product_is_sold(self, obj):
        icon = "✅" if obj.product.is_sold else "❌"
        return format_html(icon)
    product_is_sold.short_description = "Продан"



@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    inlines = [OrderProductItemInline]
    list_display = ("main_text", "active")
    def list_products(self, obj):
        return format_html(
            "<br>".join([f"{p.name} ({p.article_number})" for p in obj.products.all()])
        )

    list_products.short_description = "Выбранные товары"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            all_fields = [f.name for f in self.model._meta.fields]
            return [f for f in all_fields if f != "active" and f != "auto_complete"]
        return super().get_readonly_fields(request, obj)

    def main_text(self, obj):
        local_created = localtime(obj.created_at)
        return f"Заявка на {obj.name} от {local_created.strftime('%d-%m-%Y %H:%M:%S')}"

    main_text.short_description = "Заявка"

    def has_add_permission(self, request):
        return False


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        return False


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name",)

    def has_change_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_change_permission(request, obj)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name",)

    def has_change_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_change_permission(request, obj)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # def has_change_permission(self, request, obj=None):
    #     if obj and obj.is_sold:
    #         return False
    #     return super().has_change_permission(request, obj)
    
    list_display = (
        "name",
        "sale_price_formatted",
        "price_with_discount_formatted",
        "discount_formatted",
        "is_sold",
        "available",
        "updated_at",
    )
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("name", "slug", "article_number", "category", "brand")},
        ),
        ("Цены", {"fields": ("price", "sale_price", "discount")}),
        (
            "Характеристики",
            {"fields": (("width", "height", "depth"), "color", "material")},
        ),
        ("Внешний вид", {"fields": ("image", "description")}),
        ("Статус продажи", {"fields": ("available", "is_sold", "date_sold")}),
        (
            "Служебные данные",
            {
                "fields": ("updated_at","created_at"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("updated_at",'created_at')
    list_filter = ("available", "is_sold", "category", "brand", "color", "material")
    search_fields = ("name", "article_number", "slug")

    def price_with_discount_formatted(self, obj):
        return f"{obj.price_with_discount} ₽"

    price_with_discount_formatted.short_description = "Стоимость со скидкой"

    def sale_price_formatted(self, obj):
        return f"{obj.sale_price} ₽"

    sale_price_formatted.short_description = "Стоимость продажи"

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
