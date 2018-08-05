from django.db import models

# Create your models here.

class CYJ_admin(models.Model):
    # 管理员不使用django自带后台管理
    adname = models.CharField(max_length=50,verbose_name="管理员")
    adpassword = models.IntegerField(verbose_name="密码")

    class Meta:
        db_table = "admin"