import json
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from api.common_function import ajax_post,get_furnitures
from cyj_furniture.models import TypeInfo

# Create your views here.

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

