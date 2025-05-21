from django.urls import path
from crm.views import index
urlpatterns = [
    path("",index,name="crm_index"),
]
