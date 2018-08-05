from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CYJ_user(models.Model):
    uname = models.CharField(max_length=50,verbose_name="用户名")
    upassword = models.CharField(max_length=100,verbose_name="密码")
    uemail = models.EmailField(unique=True,null=False,verbose_name="邮箱")

    # 关联django自带用户，以便之后的登录登出装饰器
    user = models.ForeignKey(User)

    def to_dict(self):
        return dict(uid=self.id,
                    uname=self.uname,
                    upassword=self.upassword,
                    uemail=self.uemail)

    class Meta:
        db_table = "user"