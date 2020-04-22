import logging

from django.db import models
from django.db.models import Count, Sum

logger = logging.getLogger(__name__)


class SummaryQuerySet(models.QuerySet):
    """Pending Field QuerySet."""

    def filter_summary(self):
        """Filter summarty.
        Return:
            Queryset: queryset with values for summary
        """
        return self.values(
            'type_transaction', 'amount', 'account'
        ).annotate(
            Count('type_transaction'), Sum('amount')
        )

    def filter_summary_category(self):
        """Filter summarty.
        Return:
            Queryset: queryset with values for summary
        """
        return self.values_list(
            'category', 'type_transaction',
        ).annotate(
            Sum('amount')
        )


class TransactionManager(models.Manager):
    """Pending Field Manager."""

    def get_queryset(self):
        """Get queryset.
        Return:
            Queryset: Queryset.
        """
        return SummaryQuerySet(
            self.model, using=self._db
        )
