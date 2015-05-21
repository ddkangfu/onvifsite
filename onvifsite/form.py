# coding: utf-8

from django import forms


class Login(forms.Form):
    ip = forms.IPAddressField(label='HostIP:')
    port = forms.CharField(max_length=5, label='port')
    username = forms.CharField(max_length=20, label='username')
    password = forms.CharField(max_length=20, label='password')