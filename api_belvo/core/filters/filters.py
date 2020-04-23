import logging

import coreapi
from django.utils.translation import ugettext_lazy as _
from rest_framework import filters
from rest_framework.compat import coreschema
from rest_framework.exceptions import ParseError
from schema import And, Regex, Schema, Use

logger = logging.getLogger(__name__)


class RangeDateFilter(filters.BaseFilterBackend):
    """Filtering fields."""

    schema = Schema(
        And(
            Use(str),
            Regex(r'^\d{4}-\d{2}-\d{2}$')
        )
    )

    INVALID_DATE = _('The date is not valid')

    def get_schema_fields(self, view):
        """."""
        schema_cls = coreschema.String
        return [
            coreapi.Field(
                name='r_d_date',
                required=False,
                location='query',
                schema=schema_cls(
                    title=_("Date range"),
                    description=_(
                        "Filter events between dates in range. Format: "
                        "YYYY-MM-DD"
                    )
                )
            ),

        ]

    def filter_queryset(self, request, queryset, view):
        """We override to validate the dates and complement the query..
        Args:
            request(Request): Request of view.
            queryset(QuerySet): Queryset
            view(View): View from where the function is called
        Return:
            Queryset: queryset
        """
        date_range = request.GET.get('r_d_date')
        date_range_filters = {}
        if date_range is not None:
            from_date, _, to_date = date_range.partition(',')
            if from_date:
                if not self.is_valid_format(from_date):
                    raise ParseError(
                        {
                            'r_d_date': self.INVALID_DATE
                        }
                    )
                date_range_filters.update(
                    {
                        'date__gte': from_date
                    }
                )
            if to_date:
                if not self.is_valid_format(to_date):
                    raise ParseError(
                        {
                            'r_d_date': self.INVALID_DATE
                        }
                    )
                date_range_filters.update(
                    {
                        'date__lte': to_date
                    }
                )
        queryset = queryset.filter(**date_range_filters)
        return queryset

    @classmethod
    def is_valid_format(cls, date):
        """Validate the format of the dates.
        Args:
            date(Str): Date to validate.
        Return:
            Boolean: True if it is a valid date.
        """
        return cls.schema.is_valid(date)
