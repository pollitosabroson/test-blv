import json
import logging
import random

import pytest
from django.urls import reverse
from rest_framework import status

from core.utils import parse_response_content
from transactions.schemas import conf_schema_transaction
from users.models import User

logger = logging.getLogger(__name__)


@pytest.mark.django_db
@pytest.mark.urls('api_belvo.urls')
class TestCreateTransactions:
    """Specific tests for creating a user."""

    url = reverse('transactions:create_transaction')

    DATES = [
        '2020-01-15', '2020-01-23', '2020-02-24',
        '2020-03-25', '2020-02-15',
    ]

    CATEGORY_OUT = [
        'foodl', 'alcoholl', 'retail', '"groceries"'
    ]

    CATEGORY_INT = [
        'salary', 'transfer', 'investment'
    ]

    @staticmethod
    def get_success_fixtures():
        """User list for cases where the endpoint have an answer success
        """
        f_user = User.objects.first().id
        l_user = User.objects.last().id
        return [
            [
                TestCreateTransactions.get_out_fake_transaction(
                    reference=123456,
                    account=1233456,
                    user=f_user
                )
                for x in range(10)
            ] + [
                TestCreateTransactions.get_in_fake_transaction(
                    reference=456789,
                    account=456789,
                    user=l_user
                )
                for x in range(5)
            ]
        ]

    @classmethod
    def get_out_fake_transaction(cls, reference, account, user):
        """Create out fake transaction."""
        reference += random.choice(
            [x for x in range(10)]
        )
        return {
            "reference": str(reference),
            "account": str(account),
            "date": str(random.choice(cls.DATES)),
            "amount": str(round(random.uniform(10, 5000), 2)),
            "type": "outflow",
            "category": str(random.choice(cls.CATEGORY_OUT)),
            "user_id": str(user)
        }

    @classmethod
    def get_in_fake_transaction(cls, reference, account, user):
        """Create in fake transaction."""
        reference += random.choice(
            [x for x in range(100)]
        )
        return {
            "reference": str(reference),
            "account": str(account),
            "date": str(random.choice(cls.DATES)),
            "amount": str(round(random.uniform(10, 5000), 2)),
            "type": "inflow",
            "category": str(random.choice(cls.CATEGORY_INT)),
            "user_id": str(user)
        }

    def make_post_request(self, client, params=None, **keargs):
        """
        Make the request to the endpoint and return the content and status
        """
        headers = {
            'content_type': 'application/json'
        }
        i_params = params or []
        body = json.dumps(i_params)
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
            response_content, response_status = self.make_post_request(
                client,
                params=fixtures
            )
            assert status.HTTP_201_CREATED == response_status
            for transaction in response_content:
                assert conf_schema_transaction.validate(transaction)
                assert conf_schema_transaction.is_valid(transaction)
