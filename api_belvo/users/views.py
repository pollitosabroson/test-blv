from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    """USer Crear and list user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
