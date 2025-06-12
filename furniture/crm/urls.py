from django.urls import path
from crm import views
urlpatterns = [
    path("",views.index,name="crm_index"),
    path("views/",views.view_count,name="view_count")
]
