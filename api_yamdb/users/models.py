from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    RANKS = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    rank = models.CharField(choices=RANKS, max_length=10, default='user')