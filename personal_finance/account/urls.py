from django.urls import path
from rest_framework import routers

from .views import *

app_name = 'account'
router = routers.DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('create', CreateUserView.as_view({'post': 'create'})),
    path('login', LoginView.as_view())
]

urlpatterns.extend(router.urls)