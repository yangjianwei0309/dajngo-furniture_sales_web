from django.contrib import admin
from cyj_user.models import CYJ_user

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("uname","upassword",'uemail')
    list_filter = ("uname",)
    # search_fields = ("uname",)

admin.site.register(CYJ_user,UserAdmin)