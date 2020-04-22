import json
import logging
import random

import pytest
from django.urls import reverse
from rest_framework import status

from core.utils import parse_response_content
from users.schemas import conf_schema_users

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.urls('api_belvo.urls')
class TestCreateUsers:
    """Specific tests for creating a user."""

    url = reverse('users:list_create_users')

    NAMES = [
        'Zackary Knox', 'Hermione Hale', 'Darsh Joseph', 'Tevin Conroy',
        'Bjorn Hamilton', 'Asma Rice', 'Tyrique Martin', 'Zacharia Gough',
        'Belinda Adam', 'Kyran Griffiths',
    ]

    EMAILS = [
        'innerpolitisch+{}@9qwkev.com',
        'innerpolitisch+{}@cpacartago.site',
        'innerpolitisch+{}@cpacartago.hola',
        'innerpolitisch+{}@9qwkev.abc',
        'innerpolitisch+{}@cpacartago.qwe',
        'innerpolitisch+{}@cpacartago.asd',
    ]

    @staticmethod
    def get_success_fixtures():
        """User list for cases where the endpoint
        have an answer success
        """
        return [
            {
                'name': random.choice(TestCreateUsers.NAMES),
                'email': random.choice(TestCreateUsers.EMAILS),
                'age': random.choice([x for x in range(18, 99)])
            }
            for x in range(10)
        ]

    @staticmethod
    def get_bad_request_fixtures():
        """User list for cases where the endpoint
        have a fail answer
        """
        return [
            {}
        ]

    def make_post_request(self, client, params=None, **keargs):
        """
        Make the request to the endpoint and return the content and status
        """
        headers = {
            'content_type': 'application/json'
        }
        i_params = params or {}
        body = {}
        body.update(**i_params)
        body = json.dumps(body)
        response = client.post(
            self.url,
            body,
            **headers
        )
        content = parse_response_content(response)
        status = response.status_code

        return content, status

    def test_success(self, client):
        """Test to validate that a user will be edited with the parameters."""
        count = 0
        for fixtures in self.get_success_fixtures():
            count += 1
            fixtures['email'] = fixtures['email'].format(
                count
            )
            response_content, response_status = self.make_post_request(
                client,
                params=fixtures
            )
            assert status.HTTP_201_CREATED == response_status
            assert conf_schema_users.is_valid(response_content)

    def test_bad_request(self, client):
        """Test to validate that a user cannot be edited."""
        for fixtures in self.get_bad_request_fixtures():
            response_content, response_status = self.make_post_request(
                client,
                params=fixtures
            )
            assert status.HTTP_400_BAD_REQUEST == response_status
