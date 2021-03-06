from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from django.conf import settings
from .yasg import urlpatterns as doc_urls
from django.conf.urls.static import static

urlpatterns = [
    path('api/portfolio/<link>', views.PortfolioView.as_view(), name='api_portfolio'),
    path('api/user_portfolio', views.UserPortfolioListView.as_view(), name='api_user_portfolio'),
    path('api/create_portfolio', views.PortfolioCreateView.as_view(), name='api_create_portfolio'),
    path('api/create_project', views.ProjectCreateView.as_view(), name='api_create_project'),
    path('api/create_contact', views.ContactCreateView.as_view(), name='api_create_contact'),
    path('api/update_project/<pk>', views.ProjectUpdateRemoveView.as_view(), name='api_update_project'),
    path('api/update_contact/<pk>', views.ContactUpdateRemoveView.as_view(), name='api_update_contact'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls

if not settings.REACT_FRONTEND:
    urlpatterns += [
        path('register/', views.register, name='register'),
        path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
        path('reset_password/',
            auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'),
            name='reset_password'),
        path('reset_password_sent/',
            auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'),
            name='password_reset_done'),
        path('reset/<uidb64>/<token>/',
            auth_views.PasswordResetConfirmView.as_view(template_name='main/reset.html'),
            name='password_reset_confirm'),
        path('reset_password_complete/',
            auth_views.PasswordResetCompleteView.as_view(template_name='main/reset_password_complete.html'),
            name='password_reset_complete'),

        path('portfolio/<portfolio_name>', views.portfolio, name='portfolio'),
        path('', views.home, name='home'),
        path('create_portfolio/', views.create_portfolio, name='create_portfolio'),
        path('change_portfolio/<slug>/', views.change_portfolio, name='change_portfolio'),
        path('change_about_me/<int:pk>/', views.UpdateAboutMe.as_view(), name='change_about_me'),
        path('change_project/<int:pk>/', views.UpdateProject.as_view(), name='change_project'),
        path('change_contact/<int:pk>/', views.UpdateContact.as_view(), name='change_contact'),
        path('create_project/<slug>/', views.CreateProject.as_view(), name='create_project'),
        path('create_contact/<slug>/', views.CreateContact.as_view(), name='create_contact'),
        path('delete_project/<int:pk>/', views.DeleteProject.as_view(), name='delete_project'),
        path('delete_contact/<int:pk>/', views.DeleteContact.as_view(), name='delete_contact'),
        path('delete_portfolio/<int:pk>/', views.DeletePortfolio.as_view(), name='delete_portfolio'),
        path('profile/', views.profile, name='profile'),
    ]

else:
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('', views.index, name='index'),
        re_path(r'^(?:.*)/?$', views.index),
    ]
