# create all decorators here
from django.shortcuts import redirect,reverse

def after_login(func):
    def wraper(request,*args,**kwargs):
        # 已经登录
        if request.session.get("cyj_user"):
            return func(request,*args,**kwargs)
        else:
            return redirect(reverse("u_login"))
    return wraper