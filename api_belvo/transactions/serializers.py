import logging

from rest_framework import serializers

from users.models import User

from .models import Transaction

logger = logging.getLogger(__name__)


class BaseTransactionSerializer(serializers.ModelSerializer):
    """Base Tranaction Serializer."""

    reference = serializers.CharField(
        min_length=6
    )
    account = serializers.CharField(
        min_length=6
    )
    date = serializers.CharField()
    amount = serializers.CharField()
    type = serializers.CharField(
        source='type_transaction'
    )
    category = serializers.CharField()
    user_id = serializers.CharField(
        source='user.id'
    )

    class Meta:
        """Meta class for User Serializer."""

        model = Transaction
        fields = (
            'reference', 'account', 'date', 'amount',
            'type', 'category', 'user_id',
        )


class CreateTransactionSerializer(BaseTransactionSerializer):
    """User Serializer."""

    def to_internal_value(self, data):
        """Parse values for internal params.
        Args:
            data(Dict): dict whit values from serlializers
        Return:
            Dict: dict parse values
        """
        type_transaction = data.pop('type', None)
        data.update(
            {
                'type_transaction': Transaction.parte_type_transaction_name_to_int(  # NOQA
                    type_transaction
                )
            }
        )
        # Validate user exists in the platform
        user_id = data.pop('user_id', None)
        try:
            user = User.objects.get(id=user_id)
            data.update(
                {
                    'user': user
                }
            )
        except Exception:
            raise serializers.ValidationError({
                'user_id': 'User does not exist'
            })
        return data

    def to_representation(self, instance):
        """To representation serialiers.
        Args:
            instance(Dict): dict whit values from serlializers
        Return:
            Dict: Parse to representacion values.
        """
        if isinstance(instance, dict):
            instance.update(
                {
                    'user_id': str(instance.pop('user').id)
                }
            )
            instance.update(
                {
                    'type': Transaction.parte_type_transaction_int_to_name(
                        instance.pop('type_transaction')
                    )
                }
            )

        return instance

    def create(self, validated_data):
        """Create Transaction.
        Args:
            validated_data(Dict): Serializer Fields
        Return:
            Dict: Serializer Fields
        """
        Transaction.create_bulk(
            [validated_data]
        )
        return validated_data


class ListUserTransactionSerializer(BaseTransactionSerializer):
    """List User Transaction Serializer."""

    def to_representation(self, instance):
        """To representation serialiers.
        Args:
            instance(Dict): dict whit values from serlializers
        Return:
            Dict: Parse to representacion values.
        """
        instance = super(
            ListUserTransactionSerializer, self
        ).to_representation(instance)
        instance.update(
            {
                'type': Transaction.parte_type_transaction_int_to_name(
                    int(instance.get('type'))
                )
            }
        )
        return instance


class SummaryTransactionsSerializer(serializers.Serializer):
    """ SummaryTransaction."""

    account = serializers.CharField()
    balance = serializers.CharField()
    total_inflow = serializers.CharField()
    total_outflow = serializers.CharField()
