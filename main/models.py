from django.db import models
from django.contrib.auth.models import User
import uuid


class Portfolio(models.Model):
    image = models.ImageField(null=True)
    header = models.CharField(max_length=50, default='Header')
    about_me = models.TextField(default='about me')
    link = models.SlugField(max_length=30, default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    image = models.ImageField()
    project_link = models.URLField(default='/')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class Contact(models.Model):
    social_network = models.CharField(max_length=50)
    link = models.CharField(max_length=60)
    logo = models.ImageField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
