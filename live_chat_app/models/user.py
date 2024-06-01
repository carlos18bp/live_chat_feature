from django.db import models

class User(models.Model):
    """
    Model representing a user.

    Attributes:
        email (str): The email of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        is_admin (bool): Indicates whether the user has administrative privileges. Default is False.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

