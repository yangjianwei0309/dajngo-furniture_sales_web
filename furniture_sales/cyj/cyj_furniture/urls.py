from django.conf.urls import url
from cyj_furniture import views

urlpatterns = [
    url(r'^wofang/',views.wf_show,name="wf"),
    url(r'^keting/',views.kt_show,name="kt"),
    url(r'^canting/',views.ct_show,name="ct"),
    url(r'^shufang/',views.sf_show,name="sf"),
    url(r'^search/list/',views.search,name="search"),
]