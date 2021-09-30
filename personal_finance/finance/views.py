# Create your views here.
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import FinanceAccount
from .serializers import UserAccountSerializer


class CreateAccountView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = UserAccountSerializer
    queryset = FinanceAccount.objects.filter()

    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return dict(
            user=self.request.user,
        )
