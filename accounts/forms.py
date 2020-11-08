#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: superstrongz
@license: MIT Licence
@contact: 857508399@qq.com
@site: http://www.superstrongz.com/
@software: PyCharm
@file: forms.py
@time: ??
"""
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import widgets
from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = widgets.TextInput(attrs={'placeholder': "username", "class": "form-control"})
        self.fields['password'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})


class RegisterForm(UserCreationForm):
    # home_address = forms.CharField(
    #     label="家庭地址",
    #     strip=False,
    #     widget=widgets.TextInput(attrs={'placeholder': "家庭地址", "class": "form-control"}))
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(attrs={'placeholder': "用户名", "class": "form-control"})
        self.fields['email'].widget = widgets.EmailInput(attrs={'placeholder': "邮箱", "class": "form-control"})
        # self.fields['password1'].widget = widgets.PasswordInput(
        #     attrs={'placeholder': "请输入密码", "class": "form-control"})
        # self.fields['password2'].widget = widgets.PasswordInput(
        #     attrs={'placeholder': "请再次输入密码", "class": "form-control"})
        self.fields['home_address'].widget = widgets.TextInput(attrs={'placeholder': "家庭地址", "class": "form-control"})
        self.fields['home_address'].widget = widgets.TextInput(attrs={'placeholder': "家庭地址", "class": "form-control"})


    class Meta:
        model = get_user_model()
        fields = ("username", "email","home_address","nickname")
        # exclude = []
