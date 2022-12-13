from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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