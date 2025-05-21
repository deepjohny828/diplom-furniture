from django.shortcuts import render,HttpResponse,redirect
from crm.forms import ElementProductForm
from crm.models import ElementProduct
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator


def index(request):
    if request.method == "POST":
        form = ElementProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crm_index")
        else:
            return JsonResponse({'success': False,'errors':form.errors})
    form = ElementProductForm()
    elements = ElementProduct.objects.all().order_by("date_created")
    # elements_mounth = ElementProduct.objects.filter("")
    pag = Paginator(elements,10)
    page_number = request.GET.get("page")
    page_obj = pag.get_page(page_number)
    return render(request,"crm/main.html",{"form":form,"elements":page_obj})
