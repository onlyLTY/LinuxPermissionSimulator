from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


# Create your views here.

def index(request):
    return render(
        request,
        "login/login.html",
    )


def check(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect("manager:manager")
            response.set_cookie("username", username, max_age=3600)
            return response
        else:
            return render(
                request,
                "login/login.html",
                {
                    "error_message": "请检查用户名或者密码",
                },
            )

    if request.method == 'GET':
        return render(
            request,
            "login/login.html",
            {
                "error_message": "请输入用户名或者密码",
            },
        )
