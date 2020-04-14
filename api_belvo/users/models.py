from django.db import models  # NOQA
from django.utils.translation import ugettext_lazy as _

from core.models.time_stamped import TimeStampedModel


class User(TimeStampedModel):
    """User model."""

    name = models.TextField(
        _('name'),
        help_text=_('Name for user'),
        null=True, blank=True
    )
    email = models.EmailField(
        _('email address'),
        blank=True,
        unique=True,
        help_text=_('I stand out in that an e-mail is stored')
    )
    age = models.IntegerField(
        _('age'),
        default=0,
        help_text=_('Age of users')
    )
