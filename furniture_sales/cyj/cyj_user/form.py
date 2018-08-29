from django import forms
from cyj_user.models import CYJ_user

class UserForm(forms.ModelForm):
    class Meta:
        model = CYJ_user
        fields = ('uname','upassword','uemail')
