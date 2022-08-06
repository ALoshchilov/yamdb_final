from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models

from api.settings import USER_ME
from .settings import ADMIN, MODERATOR, USER, USER_ROLES


class CustomUser(AbstractUser):
    """Модель CustomUser управления пользователями."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        validators=[EmailValidator],
        verbose_name='EMail')
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='О себе'
    )
    role = models.CharField(
        max_length=50,
        choices=USER_ROLES,
        default=USER,
        verbose_name='Роль'
    )
    confirmation_code = models.IntegerField(
        default=0,
        verbose_name='Код подтверждения'
    )

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_powereduser(self):
        return self.role in [MODERATOR, ADMIN]

    class Meta(AbstractUser.Meta):
        ordering = ['username']

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact=USER_ME),
                name="reserve_USER_ME"
            )
        ]

    def __str__(self):
        return self.email
