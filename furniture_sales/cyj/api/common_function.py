from django.http import HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from cyj_furniture.models import Furniture,TypeInfo
from cyj_user.models import CYJ_user

def ajax_post(request):
    """
    给ajax技术提供的请求接口
    :param request:
    :return:
    """
    # 判断用户是否登录
    if request.session.get("cyj_user"):
        data_str = request.body.decode()
        id = data_str.split("=")[-1]
        # print(id)
        # 接受对象id完毕
        # 得到当前登录的对象
        cyj_user = CYJ_user.objects.get(uname=request.session["cyj_user"]['uname'])
        # 得到一个对应id的furniture实例
        furniture = cyj_user.furniture_set.filter(id=id).first()
        # 如果用户没有这个家具对象,创建并添加
        if furniture is None or "":
            new_furniture = Furniture.objects.get(id=id)
            # 新创建的对象默认不被收藏
            new_furniture.isfavorite = 1
            cyj_user.furniture_set.add(new_furniture)
            # 对应id的家具对象被添加到用户下
            return HttpResponse("收藏成功")
        else:
            # 直接删除用户下的这个对象
            cyj_user.furniture_set.remove(furniture)
            return HttpResponse("取消成功")

    return HttpResponse("请先登录！")

"""
以分页形式来获取家具商品的信息
"""
def get_furnitures(request,category):
    typelist = TypeInfo.objects.all()
    # 获取所有对象
    furnitures = typelist[category].furniture_set.order_by("-sales")
    furniture_list = []
    if request.session.get("cyj_user"):
        for furniture in furnitures:
            # 获取登录对象
            cyj_user = CYJ_user.objects.get(uname=request.session["cyj_user"]["uname"])
            user_furnitures = cyj_user.furniture_set.all()
            for user_furniture in user_furnitures:
                if furniture.id == user_furniture.id:
                    furniture.isfavorite = 1
                    break
                else:
                    furniture.isfavorite = 0
            furniture_dict = furniture.to_dict()
            furniture_list.append(furniture_dict)
    else:
        for furniture in furnitures:
            furniture.isfavorite = 0
            furniture_dict = furniture.to_dict()
            furniture_list.append(furniture_dict)
    # 实例化结果集 每一页8条数据，少于2条合并
    paginator = Paginator(furniture_list,8)
    page = request.GET.get("page")
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    # 返回列表
    return customer