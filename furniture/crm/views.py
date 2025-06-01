from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from products.models import Purchase,Product

@staff_member_required
def index(request):
    purchases = Purchase.objects.select_related("product").all()
    sales = Product.objects.filter(is_sold=True)

    elements = []

    for purchase in purchases:
        elements.append({
            'name': purchase.product.name,
            'price': float(purchase.purchase_price),
            'type_operation': "Закупки",
            'count': 1
        })
    for sale in sales:
        elements.append({
            'name':sale.name,
            'price': float(sale.sale_price),
            'type_operation': "Продажи",
            'count': 1
        })

    return render(request,"crm/main.html",{'elements':elements})

