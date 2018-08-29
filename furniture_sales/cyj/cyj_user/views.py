from django.shortcuts import render,redirect,reverse
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from cyj_user.models import CYJ_user
from api.decorators import after_login

# Create your views here.

def home(request):
    if request.method == "GET":
        return render(request,'furniture/index.html')

def user_register(request):
    # get请求
    if request.method == "GET":
        return render(request,'user/user_register.html')
    elif request.method == "POST":
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
            return render(request,'user/user_register.html',error)
        cyj_user = CYJ_user(uname=username,
                            upassword=make_password(password),
                            uemail=email,
                            user_id=1)
        cyj_user.save()
        # 把信息保存到session中去。
        request.session["cyj_user"] = cyj_user.to_dict()
        return redirect(reverse("home"))


def user_login(request):
    """
    用户登录，用户有一个user索引
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request,'user/user_login.html')
    elif request.method == "POST":
        error = {}
        # 通行证，可用户名可邮箱
        passcan = request.POST.get("passcan")
        password = request.POST.get("password")

        check_user = CYJ_user.objects.filter(Q(uname=passcan)|Q(uemail=passcan)).first()
        if check_user is None:
            error["error"] = "用户/邮箱不存在"
        elif check_password(password,check_user.upassword) is False:
            error["error"] = "用户或密码不正确！"

        if error:
            return render(request,'user/user_login.html',error)
        log_user = check_user.to_dict()
        furnitures = check_user.furniture_set.filter(isfavorite=1)
        for furniture in furnitures:
            print(furniture.id)
        # 保存到session数据表且刷新存货时间
        request.session["cyj_user"] = log_user
        # favorite_furniture = check_user.furniture_set.all()
        # print(favorite_furniture)
        return redirect(reverse("home"))

@after_login
def user_logout(request):
    if request.method == "GET":
        # request.session是一个Sessionstore对象，可以直接把对应键的值删除
        del request.session["cyj_user"]
        return redirect(reverse("home"))

@after_login
def favorite_list(request):
    if request.method == "GET":
        cyj_user = CYJ_user.objects.get(uname=request.session["cyj_user"]["uname"])
        # 该用户的所有家具对象列表
        furnitures = cyj_user.furniture_set.all()
        furnitures_list = []
        for furniture in furnitures:
            furniture_dict = furniture.to_dict()
            furnitures_list.append(furniture_dict)
        # 列表作为值传到前端html渲染展示
        return render(request,'user/favorite_list.html',{"list":furnitures_list})

@after_login
def change_passwd(request):
    if request.method == "GET":
        return render(request,'user/change_passwd.html')
    elif request.method == "POST":
        # 获得当前登录的对象
        cyj_user = CYJ_user.objects.get(uname=request.session["cyj_user"]["uname"])
        error = {}
        old_passwd = request.POST.get("old_passwd")
        new_passwd1 = request.POST.get("new_passwd1")
        new_passwd2 = request.POST.get("new_passwd2")
        if check_password(old_passwd,cyj_user.upassword) is False:
            error["error"] = "原密码不正确！"
        elif new_passwd1 != new_passwd2:
            error["error"] = "两次密码输入不一致！"
        if error:
            return render(request,'user/change_passwd.html',error)
        cyj_user.upassword = make_password(new_passwd2)
        cyj_user.save()
        return redirect(reverse("u_login"))
        

def publish(request,id):
    data = request.body.decode()
    try:
        cyj_user = CYJ_user.objects.get(pk=id)
    except:
        pass


