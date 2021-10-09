# Generated by Django 3.2.7 on 2021-10-09 18:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_portfolio_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='about_me',
            field=models.TextField(default='about me'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='header',
            field=models.CharField(default='Header', max_length=50),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='link',
            field=models.SlugField(default=uuid.uuid4, max_length=30, unique=True),
        ),
    ]
