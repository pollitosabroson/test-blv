# -*- coding: utf-8 -*-
from django.conf.urls import url

from users import views

app_name = 'users'
urlpatterns = [
    url(
        r'^$',
        views.UserListCreateViewSet.as_view(),
        name='list_create_users'
    ),
    url(
        r'^(?P<user_id>[-.\w]+)/transactions$',
        views.UserTransactionViewSet.as_view(),
        name='user_transaction'
    ),
]
