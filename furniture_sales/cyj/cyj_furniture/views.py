import json
import logging
from django.db.models import Sum
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from api.common_function import ajax_post,get_furnitures
from cyj_furniture.models import TypeInfo, Furniture, Cart
from cyj_user.models import CYJ_user

# Create your views here.
from cyj_user.models import Comment
# 日志对象
logger = logging.getLogger('mdjango')

@csrf_exempt
def furniture_show(request,tag_id):
    if request.method == "GET":
        # 家具商品的展示
        tag_id = int(tag_id)
        furnitures = get_furnitures(request,category=tag_id-1)
        try:
            typeof = TypeInfo.objects.all()
            type = TypeInfo.objects.get(pk=tag_id)
            fname = type.fstyle
            id = type.id
        except Exception as e:
            logging.getLogger().error(e)
        return render(request,'furniture/furnitures_show.html',{"list":furnitures,"name":fname,"typeof":typeof,
                                                                "tag_id":id})

    elif request.method == "POST":
        return ajax_post(request)

@csrf_exempt
def wf_show(request):
    if request.method == "GET":
        # 该页的家具
        p_furnitures = get_furnitures(request,category=0)
        # print(type(p_furnitures.object_list))
        return render(request, 'furniture/wf_show.html', {"list":p_furnitures})

    # 给ajax技术提供的请求接口
    elif request.method == "POST":
        return ajax_post(request)

@csrf_exempt
def kt_show(request):
    if request.method == "GET":
        p_furnitures = get_furnitures(request, category=1)
        # print(type(p_furnitures.object_list))
        return render(request, 'furniture/kt_show.html', {"list": p_furnitures})

    elif request.method == "POST":
        return ajax_post(request)

@csrf_exempt
def ct_show(request):
    if request.method == "GET":
        p_furnitures = get_furnitures(request, category=2)
        # print(type(p_furnitures.object_list))
        return render(request, 'furniture/ct_show.html', {"list": p_furnitures})

    elif request.method == "POST":
        return ajax_post(request)

@csrf_exempt
def sf_show(request):
    if request.method == "GET":
        p_furnitures = get_furnitures(request, category=3)
        # print(type(p_furnitures.object_list))
        return render(request, 'furniture/sf_show.html', {"list": p_furnitures})

    elif request.method == "POST":
        return ajax_post(request)

def search(request):
    keywords = request.POST.get("search")
    if keywords == None:
        return render(request,"furniture/index.html",{"error":"请输入关键字"})
    typelist = TypeInfo.objects.all()
    # furnitures = []
    # 获取所有家具种类索引下的所有家具对象
    # for i in range(len(typelist)):
    #     type_furnitures = typelist[i].furniture_set.all()
    #     for type_furniture in type_furnitures:
    #         furnitures.append(type_furniture)
    searcheds_list = []
    for i in range(len(typelist)):
        searcheds = typelist[i].furniture_set.filter(content__contains=keywords)
        # 判断有没有找到
        if searcheds:
            for searched in searcheds:
                searched_dict = searched.to_dict()
                searcheds_list.append(searched_dict)
        continue
    if searcheds_list:
        return render(request,'furniture/list.html',{"search_list":searcheds_list})
    return HttpResponse("没有找到相关信息")

@csrf_exempt
def detail(request,id):
    if request.method == "GET":
        furniture = Furniture.objects.get(pk=id)
        comments = Comment.objects.filter(furniture_id=id).order_by("-created_time")
        return render(request,'furniture/show_detail.html',locals())
    elif request.method == "POST":
        if request.session.get("cyj_user"):
            data = request.body.decode()
            content = json.loads(data).get("content")
            # print(content)
            # print(request.session.get("cyj_user"))
            comment = Comment(content=content,user_id=request.session.get("cyj_user").get("uid"),
                              furniture_id=id)
            # 保存到数据库
            comment.save()
            return HttpResponse("发表成功!",status=201)
        else:
            return HttpResponse("请先登录!",status=401)

@csrf_exempt
def reply(request,id):
    b_comment = Comment.objects.get(pk=id)
    b_content = b_comment.content
    b_user = b_comment.user.uname
    t_content = json.loads(request.body.decode()).get('content')
    if request.session.get("cyj_user"):
        comment = Comment(content=t_content,
                          user_id=request.session.get("cyj_user").get("uid"),
                          furniture_id=b_comment.furniture_id)
        comment.save()
        return HttpResponse(json.dumps({"data":{"b_content":b_content,
                                                "b_user":b_user,
                                                "t_content":t_content,
                                                "t_user":request.session.get("cyj_user").get("uname")}},
                                       ensure_ascii=False),content_type="application/json",charset="utf-8")
    else:
        return HttpResponse("请先登录")

def tocart(request):
        if request.session.get("cyj_user"):
            cyj_user = CYJ_user.objects.get(pk=request.session.get("cyj_user").get("uid"))
            address = cyj_user.deliveryaddress_set.get(user_id=request.session.get("cyj_user").get("uid"))
            carts = cyj_user.cart_set.filter(user_id=request.session.get("cyj_user").get("uid"))
            totalPrice = 0
            for cart in carts:
                if cart.isSelected:
                    totalPrice += cart.goods.price * cart.cnt
            return render(request,'furniture/cart.html',locals())
        else:
            return JsonResponse({"msg":"未登录，请先登录"},status=401,safe=False)

def addtocart(request,id):
    if request.session.get("cyj_user"):
        try:
            furniture = Furniture.objects.get(pk=id)
            cart = Cart(cnt=1, isSelected=1, goods_id=furniture.id,
                user_id=request.session.get("cyj_user").get("uid"))
            cart.save()
            return JsonResponse({"msg":"success"},status=200,safe=False)
        except Exception as e:
            logger.info(e)
    else:
        return JsonResponse({"msg":"未登录，请先登录"},status=401,safe=False)




def selectCart(request,cart_id):
    carts = Cart.objects.filter(user_id=request.session.get("cyj_user").get("uid"))
    if int(cart_id) == 0:
        carts.update(isSelected=1)
        totalPrice = 0
        for cart in carts:
            totalPrice += cart.cnt * cart.goods.price
        return JsonResponse({"price":totalPrice,"msg":"全部选择更新"},status=200,safe=False)
    elif int(cart_id) == 9999:
        carts.update(isSelected=0)
        totalPrice = 0
        return JsonResponse({"price":totalPrice,"msg":'全部取消选择'},status=200,safe=False)
    data = {"status": 200, 'price': 1000}
    try:
        cart = Cart.objects.get(id=cart_id)
        cart.isSelected = not cart.isSelected
        cart.save()
        data['price'] = cart.cnt*cart.goods.price
        data['selected'] = cart.isSelected # 当前选择状态
    except:
        data['status'] = 300
        data['price'] = 0
    return JsonResponse(data)


def addgoods(request,id):
    cart = Cart.objects.get(pk=id)
    cart.cnt += 1
    cart.save()
    cartPrice = cart.goods.price
    return JsonResponse({"count":cart.cnt,'price':cartPrice},status=200,safe=False)

def subgoods(request,id):
    cart = Cart.objects.get(pk=id)
    if cart.cnt > 0:
        cart.cnt -= 1
        cart.save()
    else:
        cart.cnt = 0
        cart.save()
    cartPrice = cart.goods.price
    return JsonResponse({"count":cart.cnt,'price':cartPrice},status=200,safe=False)