from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CYJ_user(models.Model):
    uname = models.CharField(max_length=50,verbose_name="用户名")
    upassword = models.CharField(max_length=100,verbose_name="密码")
    uemail = models.EmailField(unique=True,null=False,verbose_name="邮箱")

    # 关联django自带用户，以便之后的登录登出装饰器
    user = models.ForeignKey(User)

    def __str__(self):
        return self.uname

    def to_dict(self):
        return dict(uid=self.id,
                    uname=self.uname,
                    upassword=self.upassword,
                    uemail=self.uemail)

    class Meta:
        db_table = "user"

class Comment(models.Model):
    content = models.CharField(max_length=500,verbose_name="内容")
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    is_delete = models.BooleanField(default=0,blank=True,verbose_name="是否删除")
    # 外键关联
    user = models.ForeignKey(CYJ_user,verbose_name="作者")
    from cyj_furniture.models import Furniture
    furniture = models.ForeignKey(Furniture,verbose_name="所属商品")

    def __str__(self):
        return self.user

    class Meta:
        db_table = "comment"