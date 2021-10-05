from django.urls import path
from .views import portfolio, home

urlpatterns = [
    path('portfolio/<portfolio_name>', portfolio, name='portfolio'),
    path('', home, name='home')
]
