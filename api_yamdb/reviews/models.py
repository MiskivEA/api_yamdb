from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(default=1,
                               validators=[
                                   MaxValueValidator(date.today().year),
                                   MinValueValidator(1)
                               ])
    description = models.CharField(max_length=256)
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              related_name='titles')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='titles')
    # TODO если SET_NULL не создается новый объект
    # blank = True,
    # null = True,
    # on_delete = models.SET_NULL

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return self.name
