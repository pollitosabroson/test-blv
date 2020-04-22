import logging

from rest_framework import generics
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.serializers import ListUserTransactionSerializer
from users.models import User
from users.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserListCreateViewSet(generics.ListCreateAPIView):
    """USer Crear and list user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserTransactionViewSet(generics.ListAPIView):
    """USer Crear and list user."""

    queryset = Transaction.objects.all()
    serializer_class = ListUserTransactionSerializer

    def list(self, request, *args, **kwargs):
        """List users transactions."""
        queryset = Transaction.objects.filter(
            user_id=kwargs.get('user_id')
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
