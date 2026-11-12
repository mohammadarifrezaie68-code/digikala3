from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django import forms
from .models import Profile


class ProductSearchForm(forms.Form):
    q = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control me-2',
            'placeholder': 'جستجوی محصول...',
            'aria-label': 'Search'
        })
    )


class UpdatUserInfo(forms.ModelForm):
    phone = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره تماس خود را وارید کنید'})
    )
    
    address1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'آدرس 1'})
    )
    address2 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'آدرس 2'})
    )
    city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شهر'})
    )
    stat = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'استان'})
    )
    zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد پستی'})
    )
    country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کشور'})
    )
    class Meta:
        model = Profile
        fields = ('phone','address1','address2','city','stat','zipcode','country')


class UpdatePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز بالای 8 کاراکتر وارید کنید'
            }
        )
    )
    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز خودرا دوباره وارید کنید'
            }
        )
    )

    
    class Meta:
        model = User
        fields = ('new_password1','new_password2')


class UpdateUserForm(UserChangeForm):
    password = None  # Remove the password field from the form
    first_name=forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خود را وارید کنید'})
        ,required=False
    )
    last_name=forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خوانواده گی خود را وارید کنید'})
        ,required=False
    )
    email=forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ایمیل خود را وارید کنید'})
        ,required=False
    )
    username=forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام کاربری خود را وارید کنید'})
        ,required=False
    )


    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')


class SinupForm(UserCreationForm):
    first_name=forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خود را وارید کنید'})
    )
    last_name=forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خوانواده گی خود را وارید کنید'})
    )
    email=forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ایمیل خود را وارید کنید'})
    )
    username=forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام کاربری خود را وارید کنید'})
    )

    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز بالای 8 کاراکتر وارید کنید'
            }
        )
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز خودرا دوباره وارید کنید'
            }
        )
    )
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')
