# Generated by Django 3.2 on 2022-12-19 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
    ]