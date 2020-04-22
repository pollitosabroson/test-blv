import logging

from rest_framework import generics, status
from rest_framework.response import Response

from core.filters import RangeDateFilter
from transactions.models import Transaction
from transactions.serializers import (  # SummaryCategorySerializer
    CreateTransactionSerializer, SummaryTransactionsSerializer
)

logger = logging.getLogger(__name__)


class CreateTransactionsViewSet(generics.CreateAPIView):
    """Create muliples transactions."""

    serializer_class = CreateTransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()


class SummaryViewSet(generics.ListAPIView):
    """Summary for transactions users."""

    queryset = Transaction.objects.all()
    serializer_class = SummaryTransactionsSerializer
    filter_backends = (RangeDateFilter, )

    def list(self, request, *args, **kwargs):
        """Summary for transactions users."""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(
            user_id=kwargs.get('user_id')
        ).filter_summary()
        data = Transaction.parse_summary(queryset)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)


class SummaryCategoryViewSet(generics.ListAPIView):
    """Summary for transactions users."""

    queryset = Transaction.objects.all()
    filter_backends = (RangeDateFilter, )

    def list(self, request, *args, **kwargs):
        """Summary for transactions users."""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(
            user_id=kwargs.get('user_id')
        ).filter_summary_category()
        data = Transaction.paser_sumary_category(queryset)
        return Response(data)
