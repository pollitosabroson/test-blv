import logging

from rest_framework import generics
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from users.models import User
from users.serializers import UserSerializer, UserTransactionSerializer

logger = logging.getLogger(__name__)


class UserListCreate(generics.ListCreateAPIView):
    """USer Crear and list user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserTransaction(generics.ListCreateAPIView):
    """USer Crear and list user."""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    get_serializer_list_class = UserTransactionSerializer

    def list(self, request, *args, **kwargs):
        logger.error(kwargs)
        user = User.objects.get(id=kwargs.get('user_id'))
        serializer = UserTransactionSerializer(user)
        return Response(serializer.data)
