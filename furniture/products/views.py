from django.shortcuts import render, get_object_or_404, HttpResponse
from products.models import Product, Category,Feedback
from products.func import str_to_decimal
from django.core.exceptions import ValidationError
from products.forms import OrderProductForm
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import Brand, Color, Material, SliderImage
from django.db.models import Q,F
from django.core.paginator import Paginator

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
    popular_products = Product.objects.filter(available=True).order_by('-views')[:4]
    return render(
        request,
        "products/index.html",
        {"products": products, "form": form, "new_products": new_products,
         "discounted_new_products": discounted_new_products,
         "slider_images": slider_images,
         "popular_products":popular_products},
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

    if f'compared_{slug}' not in request.session:
        Product.objects.filter(slug=slug).update(views=F('views') + 1)
        request.session[f'compared_{slug}'] = True
        request.session.modified = True

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
    selected_categories = request.GET.getlist('category')
    selected_brands = request.GET.getlist('brand')
    selected_colors = request.GET.getlist('color')
    selected_materials = request.GET.getlist('material')
    categories = Category.objects.all()
    category_ids = request.GET.getlist("category")  # Получаем список ID категорий
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    discount = request.GET.get("discount")
    brand_ids = request.GET.getlist("brand")  # Список ID брендов
    color_ids = request.GET.getlist("color")  # Список ID цветов
    material_ids = request.GET.getlist("material")  # Список ID материалов
    min_width = request.GET.get("min_width")
    max_width = request.GET.get("max_width")
    min_height = request.GET.get("min_height")
    max_height = request.GET.get("max_height")
    min_depth = request.GET.get("min_depth")
    max_depth = request.GET.get("max_depth")
    
    brands = Brand.objects.filter(product__isnull=False).distinct()
    colors = Color.objects.filter(product__isnull=False).distinct()
    materials = Material.objects.filter(product__isnull=False).distinct()
    
    # Начальный queryset
    products = Product.objects.filter(available=True)
    
    # Фильтрация по категориям (если выбраны)
    if category_ids:
        products = products.filter(category_id__in=category_ids)
    
    # Фильтрация по цене
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

    # Фильтрация по скидке
    if discount == "1":
        products = products.filter(discount__gt=0)
    
    # Фильтрация по брендам
    if brand_ids:
        products = products.filter(brand_id__in=brand_ids)
    
    # Фильтрация по цветам
    if color_ids:
        products = products.filter(color_id__in=color_ids)
    
    # Фильтрация по материалам
    if material_ids:
        products = products.filter(material_id__in=material_ids)
    
    # Фильтрация по габаритам
    if min_width:
        products = products.filter(width__gte=min_width)
    if max_width:
        products = products.filter(width__lte=max_width)
    if min_height:
        products = products.filter(height__gte=min_height)
    if max_height:
        products = products.filter(height__lte=max_height)
    if min_depth:
        products = products.filter(depth__gte=min_depth)
    if max_depth:
        products = products.filter(depth__lte=max_depth)
    
    # Пагинация
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "products/product_list.html",
        {
            "products": page_obj,
            "categories": categories,
            "form": form,
            "brands": brands,
            "colors": colors,
            "materials": materials,
            "min_price": min_price,
            "max_price": max_price,
            "selected_categories": selected_categories,
            "selected_brands": selected_brands,
            "selected_colors": selected_colors,
            "selected_materials": selected_materials,
        },
    )




# def product_list(request):
#     if request.method == "POST":
#         form = OrderProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             return JsonResponse({"success": False, "errors": form.errors})

#     form = OrderProductForm()
#     categories = Category.objects.all()
#     category_id = request.GET.get("category")
#     min_price = request.GET.get("min_price")
#     max_price = request.GET.get("max_price")
#     discount = request.GET.get("discount")
#     brands = Brand.objects.filter(product__isnull=False).distinct()
#     colors = Color.objects.filter(product__isnull=False).distinct()
#     materials = Material.objects.filter(product__isnull=False).distinct()
#     products = Product.objects.filter(available=True)
#     selected_category = None

#     if category_id:
#         selected_category = Category.objects.filter(id=category_id).first()
#         products = products.filter(category_id=category_id)

#     if min_price:
#         try:
#             res = str_to_decimal(min_price)
#             products = products.filter(sale_price__gte=res)
#         except ValidationError as e:
#             print(f"Ошибка в min_price: {e}")

#     if max_price:
#         try:
#             res = str_to_decimal(max_price)
#             products = products.filter(sale_price__lte=res)
#         except ValidationError as e:
#             print(f"Ошибка в max_price: {e}")

#     if discount == "1":
#         products = products.filter(discount__gt=0)

#     return render(
#         request,
#         "products/product_list.html",
#         {
#             "products": products,
#             "categories": categories,
#             "t": category_id,
#             "form": form,
#             "sel_cat": selected_category,
#             "brands":brands,
#             "colors":colors,
#             "materials":materials,
#         },
#     )


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
        if f'compared_{product_id}' not in request.session:
            Product.objects.filter(pk=product_id).update(compare_count=F('compare_count') + 1)
            request.session[f'compared_{product_id}'] = True
            request.session.modified = True
        
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
    have_compare = compare != []
    products = Product.objects.filter(id__in=compare)
    return render(request, "products/compare_view.html", {"products": products,"have_compare":have_compare})


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
        return redirect("not_group_products")

def not_group_products(request):
    group = request.session.get("group", [])
    if group == []:
        return render(request,"products/not_group_products.html")
    else:
        redirect("group_products")


def add_to_group_products(request, product_id):
    group = request.session.get("group", [])
    product_is_available = Product.objects.filter(id=product_id,available=True)
    if product_is_available and product_id not in group:
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

def feedback(request):
    if request.method == "POST":
        req = request.POST['sss']
        obj = Feedback(email=req)
        obj.save()
    return redirect("index")


# Пока не реализовано
def page_not_found(request,exception):
    return render(request, 'products/404.html',status=404)