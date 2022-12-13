from datetime import date

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



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
        related_name='Автор',
    )
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text
