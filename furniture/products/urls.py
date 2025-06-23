from django.urls import path
from products import views

urlpatterns = [
    path("",views.index,name="index"),
    path("not_group_products/",views.not_group_products,name="not_group_products"),
    path("products/",views.product_list,
         name='product_list'),
    path("privacy_policy/",views.privacy_policy,name="privacy_policy"),
    path("product_detail/<slug:slug>/",views.product_detail,name="product_detail"),
    path("contacts/",views.contacts,name='contacts'),
    path("compare/",views.compare_view,name="compare_view"),
    path("compare/add/<int:product_id>",views.add_to_compare,name="add_to_compare"),
    path("compare/remove/<int:product_id>",views.remove_from_compare,name="remove_from_compare"),
    path("group_products/",views.group_products, name='group_products'),
    path("group_products/add/<int:product_id>",views.add_to_group_products,name="add_to_group_products"),
    path("group_products/remove/<int:product_id>",views.remove_from_group_products,name="remove_from_group_products"),
    path('search/', views.product_search, name='product_search'),
]



