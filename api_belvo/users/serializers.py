from rest_framework import serializers

from transactions.serializers import TransactionSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """User Serializer."""

    name = serializers.CharField()
    email = serializers.EmailField()
    age = serializers.IntegerField(
        min_value=0,
        max_value=99
    )

    class Meta:
        """Meta class for User Serializer."""

        model = User
        fields = ('name', 'email', 'age', )


class UserTransactionSerializer(serializers.ModelSerializer):
    """User Serializer."""

    transactions = TransactionSerializer(many=True)

    class Meta:
        """Meta class for User Serializer."""

        model = User
        fields = ('name', 'email', 'age', 'transactions')
