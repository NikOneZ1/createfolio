# Generated by Django 3.2.7 on 2021-10-14 11:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20211009_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='link',
            field=models.SlugField(default=uuid.uuid4, unique=True),
        ),
    ]
