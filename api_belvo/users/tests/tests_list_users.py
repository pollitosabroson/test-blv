import logging

import pytest
from django.urls import reverse
from rest_framework import status

from core.utils import parse_response_content
from users.schemas import conf_schema_users

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.urls('api_belvo.urls')
class TestListUsers:
    """Specific tests to make a list user"""

    url = reverse('users:list_create_users')

    @staticmethod
    def get_success_fixtures():
        """User list for cases where the endpoint
        have an answer success
        """
        return [
            {
            }
        ]

    def make_get_request(self, client, params=None, **keargs):
        """Make the request to the endpoint and return the content and status.
        """
        response = client.get(
            self.url,
        )
        content = parse_response_content(response)
        status = response.status_code

        return content, status

    def test_success(self, client):
        """Test to validate that a user will be edited with the parameters."""
        for fixtures in self.get_success_fixtures():
            response_content, response_status = self.make_get_request(
                client,
            )
            assert status.HTTP_200_OK == response_status
            for user in response_content:
                assert conf_schema_users.is_valid(user)
