from django.contrib import admin
from .models import Portfolio, Project, Contact

admin.site.register((Portfolio, Project, Contact))
