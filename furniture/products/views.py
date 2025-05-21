from django.shortcuts import render,get_object_or_404, HttpResponse
from products.models import Product, Category
from products.func import str_to_decimal
from django.core.exceptions import ValidationError
from products.forms import OrderProductForm
from django.http import JsonResponse


def index(request):
    products = Product.objects.filter(available=True)[:4]
    return render(request,'products/index.html',{'products':products})

def product_detail(request,slug):
    if request.method == "POST":
        form = OrderProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse({'success': False,'errors':form.errors})
    res = get_object_or_404(Product, slug=slug,available=True)
    form = OrderProductForm()
    return render(request,"products/product_detail.html",{"product":res,"form":form})

def product_list(request):
    if request.method == "POST":
        form = OrderProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse({'success': False,'errors':form.errors})
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    selected_category = None
    if category_id:
        selected_category = Category.objects.filter(id=category_id).first()
    form = OrderProductForm()
    if category_id:
        products = products.filter(category_id=int(category_id))
    if min_price:
        try:
            res = str_to_decimal(min_price)
            products = products.filter(price__gte=res)
        except ValidationError as e:
            print(f"Ошибка: {e}")
    if max_price:
        try:
            res = str_to_decimal(max_price)
            products = products.filter(price__lte=res)
        except ValidationError as e:
            print(f"Ошибка: {e}")
    return render(
        request,
        "products/product_list.html",
        {"products": products, "categories": categories,
         "t":category_id,"form":form,"sel_cat":selected_category},
    )

def products_feedback(request,product_id):
    
    if request.method == 'POST':
        form = OrderProductForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.product = product_id
            new_request.save()
        return HttpResponse(new_request)
            
def contacts(request):
    return render(request,'products/contact.html')
