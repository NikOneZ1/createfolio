from django.db import models
from django.contrib.auth.models import User
import uuid


class Portfolio(models.Model):
    image = models.ImageField(null=True)
    header = models.CharField(max_length=50, default='Header')
    about_me = models.TextField(default='about me')
    link = models.SlugField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.header


class Project(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    image = models.ImageField(null=True)
    project_link = models.URLField(default='/')
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name


class Contact(models.Model):
    social_network = models.CharField(max_length=50)
    link = models.URLField()
    logo = models.ImageField(null=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return self.social_network
