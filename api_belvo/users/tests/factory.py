import logging

from users.models import User

logger = logging.getLogger(__name__)


class UserFactory:
    """Class in charge of creating User objects"""

    @staticmethod
    def get_user(name='Fake name', email='fake@email.com', age=18):
        """Returns a user with the received parameters.
        Args:
            name(str, Optional): Name of user
            email(str, Optional): Email of user
            age(int, Optional): Age of user
        Return:
            Instance: User Instance
        """
        if User.objects.filter(email=email).exists():
            return User.objects.get(email=email)
        data = {
            'name': name,
            'email': email,
            'age': age
        }
        user = User(**data)
        user.save()
        return user
