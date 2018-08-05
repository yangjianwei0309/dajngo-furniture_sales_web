from django.conf.urls import url
from cyj_user import views

urlpatterns = [
    url(r'login/',views.user_login,name="u_login"),
    url(r'^register/',views.user_register,name="u_register"),
    url(r'^logout/',views.user_logout,name="u_logout"),
    url(r'^favorite_list/',views.favorite_list,name="list"),
    url(r'^change_passwd/',views.change_passwd,name="change_passwd"),
]