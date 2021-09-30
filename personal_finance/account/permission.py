from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsSameUserPermission(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        user: User = request.user
        # allow for view if user not anonymous
        # and it is same
        return (
            not user.is_anonymous and
            user.id == obj.id  # NOQA
        )
#
# class FinanceIsAuthenticated(IsAuthenticated):
#
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated)
