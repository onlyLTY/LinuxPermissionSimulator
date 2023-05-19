from django.urls import path

from . import views

app_name = "manager"
urlpatterns = [
    path("", views.manager, name="manager"),
    path("read/", views.read, name="read"),
    path("write/", views.write, name="write"),
    path("execute/", views.execute, name="execute"),
    path("add/", views.add, name="add"),
]