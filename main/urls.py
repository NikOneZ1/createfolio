from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('portfolio/<portfolio_name>', views.portfolio, name='portfolio'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path('create_portfolio/', views.create_portfolio, name='create_portfolio'),
    path('change_portfolio/<slug>/', views.change_portfolio, name='change_portfolio'),
    path('change_about_me/<int:pk>/', views.UpdateChangeMe.as_view(), name='change_about_me'),
    path('change_project/<int:pk>/', views.UpdateProject.as_view(), name='change_project'),
    path('change_contact/<int:pk>/', views.UpdateContact.as_view(), name='change_contact'),
    path('create_project/<slug>/', views.CreateProject.as_view(), name='create_project'),
    path('create_contact/<slug>/', views.CreateContact.as_view(), name='create_contact'),
    path('delete_project/<int:pk>/', views.DeleteProject.as_view(), name='delete_project'),
    path('delete_contact/<int:pk>/', views.DeleteContact.as_view(), name='delete_contact')
]
