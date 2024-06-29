from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Widget

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","password1","password2"]
    

    def __init__(self, *args: str, **kwargs: str):
        super().__init__(*args, **kwargs)

        username: Widget = self.fields['username'].widget
        username.attrs.update({
            "hx-post":"/check-username/", 
            "hx-target":"#id_username_helptext", 
            "hx-trigger": "keyup changed delay:1s", 
            "class":"text-dark",
            "placeholder": "Enter your username"
        }) 

        password1: Widget = self.fields["password1"].widget
        password1.attrs.update({"placeholder": "Enter your password"})

        password2: Widget = self.fields["password2"].widget
        password2.attrs.update({"placeholder": "Enter your password"})