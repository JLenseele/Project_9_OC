# Generated by Django 4.1.6 on 2023-02-03 21:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[
                django.core.validators.MinValueValidator(0),
                django.core.validators.MaxValueValidator(5)]),
        ),
    ]
