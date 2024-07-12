from . import views
from django.urls import re_path

urlpatterns = [
    re_path('users', views.index),
    re_path('user', views.user)
]
