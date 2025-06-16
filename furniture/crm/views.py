from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from products.models import Purchase,Product
from django.core.paginator import Paginator



@staff_member_required
def index(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    purchases = Purchase.objects.select_related("product").all()
    sales = Product.objects.filter(is_sold=True)

    if start_date:
        purchases = purchases.filter(purchase_date__gte=start_date)
        sales = sales.filter(date_sold__gte=start_date)

    if end_date:
        purchases = purchases.filter(purchase_date__lte=end_date)
        sales = sales.filter(date_sold__lte=end_date)

    elements = []

    for purchase in purchases:
        elements.append({
            'name': purchase.product.name,
            'price': float(purchase.purchase_price),
            'type_operation': "Закупки",
        })
    for sale in sales:
        elements.append({
            'name':sale.name,
            'price': float(sale.sale_price),
            'type_operation': "Продажи",
        })

    paginator = Paginator(elements, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"crm/main.html",{'elements':elements,'page_obj':page_obj})



@staff_member_required
def view_count(request):
    min_views = request.GET.get('min_views')
    max_views = request.GET.get('max_views')

    # Получаем все продукты для диаграммы (без пагинации)
    all_products = Product.objects.filter(is_sold=False)

    if min_views:
        all_products = all_products.filter(views__gte=min_views)
    if max_views:
        all_products = all_products.filter(views__lte=max_views)

    # Пагинация только для таблицы
    paginator = Paginator(all_products, 25)  # 2 элемента на страницу для примера
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'all_products': all_products,  # Передаем все продукты для диаграммы
    }

    return render(request, "crm/view_count.html", context)

