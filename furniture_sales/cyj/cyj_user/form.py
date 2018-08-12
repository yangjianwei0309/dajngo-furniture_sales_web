from django.forms import ModelForm
from cyj_user.models import CYJ_user

class UserForm(ModelForm):
    class Meta:
        model = CYJ_user
        fields = ('uname','upassword','uemail')