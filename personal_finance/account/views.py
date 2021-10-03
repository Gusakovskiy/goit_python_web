from django.contrib.auth.models import User

# Create your views here.

#
# from todo.api import create_default_todo  # NOQA
# from user.api import create_user  # NOQA
from django.utils.decorators import classonlymethod

from rest_framework import mixins, renderers
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .models import *  # NOQA  should be imported to add signal
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .permission import IsSameUserPermission
from .serializers import UserSerializer


class CreateUserView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    authentication_classes = ()
    permission_classes = []
    throttle_classes = ()


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsSameUserPermission]


class LoginView(ObtainAuthToken):
    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer
    )