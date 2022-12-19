from datetime import date, datetime, timedelta

import jwt
from django.db import models
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator, RegexValidator)
from django.contrib.auth.models import AbstractUser


from api_yamdb import settings


class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$')]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=150,
        verbose_name='роль',
        choices=ROLES,
        default='user'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username


class Category(models.Model):

    name = models.CharField(max_length=256,
                            verbose_name='Категория',
                            )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')],
        verbose_name='URL'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(max_length=50, verbose_name='Жанр')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')],
        verbose_name='URL'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=128,
                            verbose_name='Название',
                            )
    year = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(date.today().year),
            MinValueValidator(1)
        ],
        verbose_name='Дата выхода',
    )
    description = models.TextField(
        max_length=256,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        through='GenreTitle',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        default='Категория не определена',
        on_delete=models.SET_DEFAULT,
        related_name='titles',
    )

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.ForeignKey(
        Title,
        verbose_name='titles',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка')
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            ),
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(
        Review,
        verbose_name='Дата публикации',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='author',
    )
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text
