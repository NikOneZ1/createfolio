from django.urls import path
from .views import home

urlpatterns = [
    path('portfolio/<portfolio_name>', home, name='home'),
]
