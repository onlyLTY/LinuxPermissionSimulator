import json
from urllib import request

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render
from .models import File


# Create your views here.

def manager(request):
    file_list = get_file_list()
    for file in file_list:
        file['permissions'] = permissions_to_string(file['permissions'])
    return render(
        request,
        "manager/manager.html",
        {
            "file_list": file_list,
        },
    )


def read(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        num = int(data.get('num'))
        file_list = get_file_list()
        file = file_list[num]
        owner = file.get('owner')
        group = file.get('group')
        permissions = file.get('permissions')
        permissions = permissions_to_string(permissions)
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)  # 获取用户
        if owner == user.__str__():
            if permissions[0] == "r":
                return HttpResponse(json.dumps({"status": "read_success"}))
            else:
                return HttpResponse(json.dumps({"status": "read_failed"}))
        elif is_user_in_group(user, group):
            if permissions[3] == "r":
                return HttpResponse(json.dumps({"status": "read_success"}))
            else:
                return HttpResponse(json.dumps({"status": "read_failed"}))
        else:
            if permissions[6] == "r":
                return HttpResponse(json.dumps({"status": "read_success"}))
            else:
                return HttpResponse(json.dumps({"status": "read_failed"}))


def write(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        num = int(data.get('num'))
        file_list = get_file_list()
        file = file_list[num]
        owner = file.get('owner')
        group = file.get('group')
        permissions = file.get('permissions')
        permissions = permissions_to_string(permissions)
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)  # 获取用户
        if owner == user.__str__():
            if permissions[1] == "w":
                return HttpResponse(json.dumps({"status": "write_success"}))
            else:
                return HttpResponse(json.dumps({"status": "write_failed"}))
        elif is_user_in_group(user, group):
            if permissions[1] == "w":
                return HttpResponse(json.dumps({"status": "write_success"}))
            else:
                return HttpResponse(json.dumps({"status": "write_failed"}))
        else:
            if permissions[2] == "w":
                return HttpResponse(json.dumps({"status": "write_success"}))
            else:
                return HttpResponse(json.dumps({"status": "write_failed"}))


def execute(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        num = int(data.get('num'))
        file_list = get_file_list()
        file = file_list[num]
        owner = file.get('owner')
        group = file.get('group')
        permissions = file.get('permissions')
        permissions = permissions_to_string(permissions)
        username = request.COOKIES.get('username')
        user = User.objects.get(username=username)  # 获取用户
        if owner == user.__str__():
            if permissions[2] == "x":
                return HttpResponse(json.dumps({"status": "execute_success"}))
            else:
                print(permissions)
                return HttpResponse(json.dumps({"status": "execute_failed"}))
        elif is_user_in_group(user, group):
            if permissions[5] == "x":
                return HttpResponse(json.dumps({"status": "execute_success"}))
            else:
                return HttpResponse(json.dumps({"status": "execute_failed"}))
        else:
            if permissions[8] == "x":
                return HttpResponse(json.dumps({"status": "execute_success"}))
            else:
                return HttpResponse(json.dumps({"status": "execute_failed"}))


def add(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        file_name = data.get('file_name')
        permissions = data.get('permissions')
        owner = request.COOKIES.get('username')
        user = User.objects.get(username=owner)
        groups = user.groups.all()
        group = groups[0]
        print('add')
        new_file = File(name=file_name, owner=user, group=group, permissions=permissions)
        new_file.save()
        return HttpResponse(json.dumps({"status": "add_success"}))
    else:
        return HttpResponse(json.dumps({"status": "add_failed"}))


def get_file_list():
    all_files = File.objects.all()
    file_list = []
    for file in all_files:
        print(file.name)
        file_info = {
            "name": file.name,
            "permissions": file.permissions,
            "owner": file.owner.username,
            "group": file.group.name,
        }
        file_list.append(file_info)
    return file_list


def is_user_in_group(user, group_name):
    """
    判断用户是否在指定的组中。

    参数:
    - user: User 实例
    - group_name: 要检查的组的名字

    返回值:
    - 如果用户在指定的组中，返回 True
    - 否则，返回 False
    """
    return user.groups.filter(name=group_name).exists()


def permissions_to_string(permissions):
    # 将整数权限拆分为三位
    permissions_str = str(permissions).zfill(3)

    # 定义权限字典
    permissions_dict = {'1': '--x', '2': '-w-', '3': '-wx', '4': 'r--', '5': 'r-x', '6': 'rw-', '7': 'rwx', '0': '---'}

    # 使用列表推导来创建权限字符串
    permissions_string = ''.join([permissions_dict[char] for char in permissions_str])

    return permissions_string
