import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from cyj_furniture.models import TypeInfo
from cyj_user.models import CYJ_user
from api.common_function import ajax_post

# Create your views here.

@csrf_exempt
def wf_show(request):
    if request.method == "GET":
        typelist = TypeInfo.objects.all()
        wofangs = typelist[0].furniture_set.order_by("-sales")[8:16]
        # print(wofangs)
        wofang_list = []
        if request.session.get("cyj_user"):
            for wofang in wofangs:
                # print(wofang)
                # 获取登录对象
                cyj_user = CYJ_user.objects.get(uname=request.session["cyj_user"]['uname'])
                furnitures = cyj_user.furniture_set.all()
                # print(furnitures)
                for furniture in furnitures:
                    if wofang.id == furniture.id:
                        wofang.isfavorite = 1
                        break
                    else:
                        wofang.isfavorite = 0
                wofang_dict = wofang.to_dict()
                wofang_list.append(wofang_dict)
            # return HttpResponse(json.dumps(wofang_dict,ensure_ascii=False),
            #                 content_type="application/json",status=201)
        else:
            for wofang in wofangs:
                wofang.isfavorite = 0
                wofang_dict = wofang.to_dict()
                wofang_list.append(wofang_dict)
        return render(request, 'furniture/wf_show.html', {"list": wofang_list})


    # 给ajax技术提供的请求接口
    elif request.method == "POST":
        return ajax_post(request)

@csrf_exempt
def kt_show(request):
    if request.method == "GET":
        typelist = TypeInfo.objects.all()
        ketings = typelist[1].furniture_set.order_by("-sales")[0:8]
        keting_list = []
        if request.session.get("cyj_user"):
            for keting in ketings:
                # print(keting)
                # 获取登录对象
                cyj_user = CYJ_user.objects.get(uname=request.session["cyj_user"]['uname'])
                furnitures = cyj_user.furniture_set.all()
                # print(furnitures)
                for furniture in furnitures:
                    if keting.id == furniture.id:
                        keting.isfavorite = 1
                        break
                    else:
                        keting.isfavorite = 0
                keting_dict = keting.to_dict()
                keting_list.append(keting_dict)
        else:
            for keting in ketings:
                keting.isfavorite = 0
                keting_dict = keting.to_dict()
                keting_list.append(keting_dict)
        return render(request, 'furniture/kt_show.html', {"list": keting_list})

    elif request.method == "POST":
        return ajax_post(request)

@csrf_exempt
def ct_show(request):
    if request.method == "GET":
        # 返回一个家具类型的list
        typelist = TypeInfo.objects.all()
        # 获取销量前8的餐厅家具对象列表
        cantings = typelist[2].furniture_set.order_by("-sales")[0:8]
        canting_list = []
        if request.session.get("cyj_user"):
            for canting in cantings:
                # print(keting)
                # 获取登录对象
                cyj_user = CYJ_user.objects.get(uname=request.session["cyj_user"]['uname'])
                furnitures = cyj_user.furniture_set.all()
                # print(furnitures)
                for furniture in furnitures:
                    if canting.id == furniture.id:
                        canting.isfavorite = 1
                        break
                    else:
                        canting.isfavorite = 0
                canting_dict = canting.to_dict()
                canting_list.append(canting_dict)
        else:
            for canting in cantings:
                canting.isfavorite = 0
                canting_dict = canting.to_dict()
                canting_list.append(canting_dict)
        return render(request, 'furniture/ct_show.html', {"list": canting_list})

    elif request.method == "POST":
        return ajax_post(request)

@csrf_exempt
def sf_show(request):
    if request.method == "GET":
        typelist = TypeInfo.objects.all()
        shufangs = typelist[3].furniture_set.order_by("-sales")[0:8]
        shufang_list = []
        if request.session.get("cyj_user"):
            for shufang in shufang:
                # print(keting)
                # 获取登录对象
                cyj_user = CYJ_user.objects.get(uname=request.session["cyj_user"]['uname'])
                furnitures = cyj_user.furniture_set.all()
                # print(furnitures)
                for furniture in furnitures:
                    if shufang.id == furniture.id:
                        shufang.isfavorite = 1
                        break
                    else:
                        shufnag.isfavorite = 0
                shufang_dict = shufang.to_dict()
                shufang_list.append(shufang_dict)
        else:
            for shufang in shufangs:
                shufang.isfavorite = 0
                shufang_dict = shufang.to_dict()
                shufang_list.append(shufang_dict)
        return render(request, 'furniture/sf_show.html', {"list": shufang_list})

    elif request.method == "POST":
        return ajax_post(request)

def is_favorite(request):
    """
    根据用户点击来确定是否收藏，再次点击可以取消收藏，如果收藏，在收藏列表里可以看到收藏的产品
    :param request:
    :return:
    """
    # if request.user:
    #     if request.method == ""
    pass
