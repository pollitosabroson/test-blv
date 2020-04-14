# -*- coding: utf-8 -*-
from django.conf.urls import url

from users import views

app_name = 'users'
urlpatterns = [
    url(
        r'^$',
        views.UserList.as_view(),
        name='list_create_users'
    ),
]
