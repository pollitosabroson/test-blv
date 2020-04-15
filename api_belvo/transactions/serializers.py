import logging

from rest_framework import serializers

from users.models import User

from .models import Transaction

logger = logging.getLogger(__name__)


class TransactionSerializer(serializers.ModelSerializer):
    """User Serializer."""

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
                'user_id': 'Dont exists user'
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
                    'user': instance.get('user').id
                }
            )
            instance.update(
                {
                    'type': Transaction.parte_type_transaction_int_to_name(
                        instance.get('type_transaction')
                    )
                }
            )
        else:
            instance = super(
                TransactionSerializer, self
            ).to_representation(instance)
            instance.update(
                {
                    'type': Transaction.parte_type_transaction_int_to_name(
                        int(instance.get('type'))
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
