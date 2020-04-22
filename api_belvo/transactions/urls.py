# -*- coding: utf-8 -*-
from django.conf.urls import url

from transactions import views

app_name = 'transactions'
urlpatterns = [
    url(
        r'^$',
        views.CreateTransactionsViewSet.as_view(),
        name='create_transaction'
    ),
    url(
        r'^(?P<user_id>[-.\w]+)$',
        views.SummaryViewSet.as_view(),
        name='summary_transaction'
    ),
    url(
        r'^(?P<user_id>[-.\w]+)/category$',
        views.SummaryCategoryViewSet.as_view(),
        name='summary_transaction_category'
    ),
]
