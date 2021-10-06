from django.urls import path
from .views import portfolio, home, register

urlpatterns = [
    path('portfolio/<portfolio_name>', portfolio, name='portfolio'),
    path('', home, name='home'),
    path('register/', register, name='register'),
]
