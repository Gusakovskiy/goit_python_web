from django.urls import path

from .views import *

app_name = 'finance'


urlpatterns = [
    path('account/', CreateAccountView.as_view(
        {
            'post': 'create',
            'list': 'retrieve',
        }
    ), name='finance_account'),
]
