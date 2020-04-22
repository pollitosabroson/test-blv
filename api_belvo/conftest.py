import logging

import pytest
from django.conf import settings

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    """Establish a connection to the database being used
    in the environment to be tested."""

    settings.DATABASES['default'] = settings.DATABASES['default']
