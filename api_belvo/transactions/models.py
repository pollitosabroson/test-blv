import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models.time_stamped import TimeStampedModel
from users.models import User

logger = logging.getLogger(__name__)


class Transaction(TimeStampedModel):
    """User model."""

    TRANSACTION_INFLOW = 10
    TRANSACTION_OUTFLOW = 20
    TRANSACTION_INFLOW_NAME = _('inflow')
    TRANSACTION_OUTFLOW_NAME = _('outflow')
    TYPE_TRANSACTIONS = (
        (TRANSACTION_INFLOW, TRANSACTION_INFLOW_NAME),
        (TRANSACTION_OUTFLOW, TRANSACTION_OUTFLOW_NAME)
    )

    reference = models.TextField(
        _('reference'),
        help_text=_('number reference'),
        unique=True
    )
    account = models.TextField(
        _('account'),
        help_text=_('I stand out in that an e-mail is stored')
    )
    date = models.DateField(
        _('Date'),
        help_text=_('Date transaction')
    )
    amount = models.DecimalField(
        _('Amount'),
        help_text=_('Amount'),
        max_digits=1000, decimal_places=2
    )
    type_transaction = models.IntegerField(
        _('status about me'),
        choices=TYPE_TRANSACTIONS,
        help_text=_('Type transaction')
    )
    category = models.TextField(
        _('Category'),
        help_text=_('Category')
    )
    user = models.ForeignKey(
        User,
        on_delete='cascade',
        related_name='transactions'
    )

    @classmethod
    def parte_type_transaction_int_to_name(cls, transaction):
        """Get name to status.
        Args:
            transaction(int): value to type transaction
        Return:
            str: name transaction
        """
        for k, v in cls.TYPE_TRANSACTIONS:
            if k == transaction:
                return v

    @classmethod
    def parte_type_transaction_name_to_int(cls, transaction):
        """Get status to name.
        Args:
            transaction(str): value to type transaction
        Return:
            str: name transaction
        """
        for k, v in cls.TYPE_TRANSACTIONS:
            if v == transaction:
                return k

    @classmethod
    def create_bulk(cls, values=None, ignore_conflicts=True):
        """Create multiples vales in bulk.
        Args:
            values(List, Optional)
            ignore_conflicts(Bool): flag for ignore conflicts
        Return:
            instances: instances created
        """
        i_values = values or []
        bulk_values = [
            cls(**x)
            for x in i_values
        ]
        results = cls.objects.bulk_create(
            bulk_values,
            ignore_conflicts=ignore_conflicts
        )
        return results
