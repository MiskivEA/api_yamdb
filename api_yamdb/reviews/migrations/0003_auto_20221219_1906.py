# Generated by Django 3.2 on 2022-12-19 16:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221216_1806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genretitle',
            old_name='genre',
            new_name='genre_id',
        ),
        migrations.RemoveField(
            model_name='genretitle',
            name='Title',
        ),
        migrations.AddField(
            model_name='genretitle',
            name='title_id',
            field=models.ForeignKey(db_column='title_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='reviews.title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(regex='^[-a-zA-Z0-9_]+$')], verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='review',
            field=models.ForeignKey(db_column='review_id', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(regex='^[-a-zA-Z0-9_]+$')], verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='genretitle',
            name='genre_id',
            field=models.ForeignKey(db_column='genre_id', on_delete=django.db.models.deletion.CASCADE, to='reviews.genre'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(db_column='title_id', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='titles'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]