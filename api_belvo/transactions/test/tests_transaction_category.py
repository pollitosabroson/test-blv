import logging

import pytest
from django.urls import reverse
from rest_framework import status

from core.utils import parse_response_content
from transactions.schemas import conf_schema_transaction_category
from users.models import User

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.urls('api_belvo.urls')
class TestSummaryUsers:
    """Specific tests sumarry transactions form users."""

    url = lambda _, user_id: reverse(
        'transactions:summary_transaction_category',
        kwargs={
            'user_id': user_id
        }
    )

    @staticmethod
    def get_success_fixtures():
        """User transactions for cases where the endpoint
        have an answer success
        """
        users = User.objects.all()
        return [
            {
                'user_id': x.id
            }
            for x in users
        ] + [
            {
                'user_id': users[0].id,
                'params': {
                    'r_d_data': '2020-01-01,2020-12-31'
                }
            },
            {
                'user_id': users[0].id,
                'params': {
                    'r_d_data': '2020-01-01,'
                }
            },
            {
                'user_id': users[0].id,
                'params': {
                    'r_d_data': '2020-12-31,'
                }
            },
        ]

    def make_get_request(self, client, user_id, params=None, **keargs):
        """Make the request to the endpoint and return the content and status.
        """
        i_params = params or {}
        response = client.get(
            self.url(user_id),
            i_params
        )
        content = parse_response_content(response)
        status = response.status_code

        return content, status

    def test_success(self, client):
        """Test to validate that a user will be edited with the parameters."""
        for fixtures in self.get_success_fixtures():
            response_content, response_status = self.make_get_request(
                client,
                **fixtures
            )
            assert status.HTTP_200_OK == response_status
            logger.error('response_content')
            logger.error(response_content)
            assert conf_schema_transaction_category.validate(response_content)
            assert conf_schema_transaction_category.is_valid(response_content)
