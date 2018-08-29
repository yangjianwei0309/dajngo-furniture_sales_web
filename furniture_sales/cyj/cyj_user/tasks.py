import random

from cyj.celery import app
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def random_str(length):
    randomStr = []
    for _ in range(length):
        x = random.randint(1, 3)
        if x == 1:
            r_str = random.randrange(ord('1'),ord('9'))
        if x == 2:
            r_str = random.randrange(ord('A'),ord('Z'))
        if x == 3:
            r_str = random.randrange(ord('a'), ord('z'))
        randomStr.append(chr(r_str))
    random_code = ''.join(i for i in randomStr)
    return random_code

@app.task
def send_email():
    subject = '注册激活邮箱'
    text_content = "请激活您的账号 --餐宜家"
    html_content = "<p>点击下方链接激活</p><br/><a>jfahshuiajb</a>"
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject,text_content,from_email,['1159409912@qq.com'])

    msg.attach_alternative(html_content,'text/html')
    msg.send()
