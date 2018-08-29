from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from cyj_user.models import CYJ_user
from api.resource import Resource

class User_Register(Resource):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/user_register.html')
    def post(self, request, *args, **kwargs):
        error = {}
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        # 从数据库里查找是否含有username和email的数据
        check_user = CYJ_user.objects.filter(uname=username).first()
        check_email = CYJ_user.objects.filter(uemail=email).first()
        if not username:
            error["error"] = "用户名不能为空"
        elif not password:
            error["error"] = "密码不能为空"
        elif not email:
            error["error"] = "邮箱不能为空"
        elif len(password) < 6:
            error["error"] = "密码不能小于6位"
        elif check_user is not None:
            error["error"] = "用户名已存在"
        elif check_email is not None:
            error["error"] = "邮箱已被使用！"

        if error:
            return render(request, 'user/user_register.html', error)
        cyj_user = CYJ_user(uname=username,
                            upassword=make_password(password),
                            uemail=email,
                            user_id=1)
        cyj_user.save()
        # 把信息保存到session中去。
        request.session["cyj_user"] = cyj_user.to_dict()
        return JsonResponse(cyj_user,status=200,safe=False)

class User_Login(Resource):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"response":"ok"})
    def post(self, request, *args, **kwargs):
        error = {}
        # 通行证，可用户名可邮箱
        passcan = request.POST.get("passcan")
        password = request.POST.get("password")

        check_user = CYJ_user.objects.filter(Q(uname=passcan) | Q(uemail=passcan)).first()
        if check_user is None:
            error["error"] = "用户/邮箱不存在"
        elif check_password(password, check_user.upassword) is False:
            error["error"] = "用户或密码不正确！"

        if error:
            return render(request, 'user/user_login.html', error)
        log_user = check_user.to_dict()
        furnitures = check_user.furniture_set.filter(isfavorite=1)
        # 保存到session数据表且刷新存货时间
        request.session["cyj_user"] = log_user
        # favorite_furniture = check_user.furniture_set.all()
        # print(favorite_furniture)
        return JsonResponse(log_user,safe=False)