from django import forms
from .models import Comments
from django.contrib.auth.models import User

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=24)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)
class CommentForm(forms.ModelForm):
    class Meta:
        model= Comments
        fields= ('name','email','body')
class signupform(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']
