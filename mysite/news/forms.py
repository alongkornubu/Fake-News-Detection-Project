from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField ,UserChangeForm
from django.contrib.auth.models import User
from .models import *

# label = "ชื่อผู้ใช้งาน"
# label = "รหัสผ่าน" 
# label = "ยืนยันรหัสผ่าน" 

class Registerform(UserCreationForm):
    username = forms.CharField(label="ชื่อผู้ใช้งาน", widget=forms.TextInput
    (attrs={'class':'rounded-sm border-2 px-4 py-3 mt-3 focus:outline-none bg-white w-full'}))
    password1 = forms.CharField(label="รหัสผ่าน", widget=forms.PasswordInput
        (attrs={'class':'rounded-sm border-2 px-4 py-3 mt-3 focus:outline-none bg-white w-full'}))
    password2 = forms.CharField(label="ยืนยันรหัสผ่าน", widget=forms.PasswordInput
        (attrs={'class':'rounded-sm border-2 px-4 py-3 mt-3 focus:outline-none bg-white w-full'}))

    class Meta:
        model = User
        fields = {'username'}

# class Loginform(AuthenticationForm):
#     username = UsernameField(label="ชื่อผู้ใช้",widget= forms.TextInput(attrs={'class':'rounded-sm px-4 py-3 mt-3 focus:outline-none bg-gray-100 w-full'}))
#     password = forms.CharField(label="รหัสผ่าน",strip=False,widget=forms.PasswordInput(attrs={'class':'rounded-sm px-4 py-3 mt-3 focus:outline-none bg-gray-100 w-full'}))

class CategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='หมวดหมู่')

class EditUserProfile(UserChangeForm):

    class Meta:
        model = User
        fields = ['username']
        pass

class Newsform(forms.ModelForm):
    
    class Meta:
        model = News
        fields = ['name','title','text','label','category','image',]
        
