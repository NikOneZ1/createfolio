from django.urls import path
from .views import portfolio, home, register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('portfolio/<portfolio_name>', portfolio, name='portfolio'),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
]
