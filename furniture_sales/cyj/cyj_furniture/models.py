from django.db import models
from cyj_user.models import CYJ_user

# Create your models here.

class TypeInfo(models.Model):
    fstyle = models.CharField(max_length=50, verbose_name="样式")

class Furniture(models.Model):
    # 家具字段
    fname = models.CharField(max_length=100,null=False,verbose_name="家具种类")
    content = models.CharField(max_length=300,verbose_name="基本信息")
    price = models.IntegerField(null=False,verbose_name="价格")
    img = models.CharField(max_length=100,null=True,verbose_name="图片名")
    sales = models.IntegerField(null=True,verbose_name="销量")
    url = models.CharField(max_length=800,null=True,verbose_name="链接")
    click = models.IntegerField(default=0,verbose_name="点击量")
    isfavorite = models.BooleanField(default=0,verbose_name="是否收藏")
    # 外键关联
    # 一个用户可以收藏多件服装，一件服装也可以被多个用户收藏
    mm_user = models.ManyToManyField(CYJ_user)
    typeinfo = models.ForeignKey(TypeInfo)

    def to_dict(self):
        return dict(id=self.id,
                    fname=self.fname,
                    content=self.content,
                    price=self.price,
                    img = self.img,
                    sales=self.sales,
                    url=self.url,
                    click=self.click,
                    isfavorite=self.isfavorite)

    class Meta:
        db_table = "furniture"


