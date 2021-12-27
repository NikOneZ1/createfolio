from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from .yasg import urlpatterns as doc_urls
from django.conf import settings
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
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    re_path(r'^(?:.*)/?$', views.index),
]

urlpatterns += doc_urls
