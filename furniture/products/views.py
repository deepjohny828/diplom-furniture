from django.shortcuts import render, get_object_or_404, HttpResponse
from products.models import Product, Category
from products.func import str_to_decimal
from django.core.exceptions import ValidationError
from products.forms import OrderProductForm
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import SliderImage
from django.db.models import Q

def index(request):
    if request.method == "POST":
        form = OrderProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    slider_images = SliderImage.objects.all()
    new_products = Product.objects.filter(available=True).order_by("-created_at")[:4]
    form = OrderProductForm()
    products = Product.objects.filter(available=True)[:4]
    discounted_new_products = Product.objects.filter(available=True, discount__gt=0).order_by('-created_at')[:4]
    return render(
        request,
        "products/index.html",
        {"products": products, "form": form, "new_products": new_products,
         "discounted_new_products": discounted_new_products,
         "slider_images": slider_images,},
    )

def product_search(request):
    query = request.GET.get('q', '')
    products = []
    
    if query:

        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(article_number__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(description__icontains=query),
            available=True
        ).distinct()
    
    return render(request, 'products/search_results.html', {
        'products': products,
        'search_query': query
    })

def product_detail(request, slug):
    if request.method == "POST":
        form = OrderProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    res = get_object_or_404(Product, slug=slug, available=True)
    form = OrderProductForm()
    return render(
        request, "products/product_detail.html", {"product": res, "form": form}
    )


def product_list(request):
    if request.method == "POST":
        form = OrderProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse({"success": False, "errors": form.errors})

    form = OrderProductForm()
    categories = Category.objects.all()
    category_id = request.GET.get("category")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    discount = request.GET.get("discount")

    products = Product.objects.filter(available=True)
    selected_category = None

    if category_id:
        selected_category = Category.objects.filter(id=category_id).first()
        products = products.filter(category_id=category_id)

    if min_price:
        try:
            res = str_to_decimal(min_price)
            products = products.filter(sale_price__gte=res)
        except ValidationError as e:
            print(f"Ошибка в min_price: {e}")

    if max_price:
        try:
            res = str_to_decimal(max_price)
            products = products.filter(sale_price__lte=res)
        except ValidationError as e:
            print(f"Ошибка в max_price: {e}")

    if discount == "1":
        products = products.filter(discount__gt=0)

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
            "t": category_id,
            "form": form,
            "sel_cat": selected_category,
        },
    )


def products_feedback(request, product_id):

    if request.method == "POST":
        form = OrderProductForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.product = product_id
            new_request.save()
        return HttpResponse(new_request)


def contacts(request):
    return render(request, "products/contact.html")


def add_to_compare(request, product_id):
    compare = request.session.get("compare", [])
    if product_id not in compare:
        compare.append(product_id)
    request.session["compare"] = compare
    return redirect("compare_view")


def remove_from_compare(request, product_id):
    compare = request.session.get("compare", [])
    if product_id in compare:
        compare.remove(product_id)
    request.session["compare"] = compare
    return redirect("compare_view")


def compare_view(request):
    compare = request.session.get("compare", [])
    products = Product.objects.filter(id__in=compare)
    return render(request, "products/compare_view.html", {"products": products})


def group_products(request):
    group = request.session.get("group", [])
    products = Product.objects.filter(id__in=group)
    if request.method == "POST":
        form = OrderProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    form = OrderProductForm()
    if group != []:
        final_price = 0
        total_discount = 0
        total_price = 0
        for product in products:
            final_price += product.price_with_discount
            total_discount += product.discount
            total_price += product.sale_price
        return render(
            request,
            "products/group_products.html",
            {
                "elements": products,
                "final_price": final_price,
                "total_price": total_price,
                "total_discount": total_discount,
                "form": form,
            },
        )
    else:
        return redirect("/")


def add_to_group_products(request, product_id):
    group = request.session.get("group", [])
    if product_id not in group:
        group.append(product_id)
    request.session["group"] = group
    return redirect("group_products")


def remove_from_group_products(request, product_id):
    group = request.session.get("group", [])
    if product_id in group:
        group.remove(product_id)
    request.session["group"] = group
    if group != []:
        print(len(request.session["group"]))
        return redirect("group_products")
    else:
        return redirect("/")
