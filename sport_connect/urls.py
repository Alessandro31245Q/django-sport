"""
URL configuration for sport_connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from sports import views as SportsViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('category/', include('sports.urls')),
    path('courts/', include('sports.urls')),
    path('sport/<slug:slug>', SportsViews.sports, name='sports'),
    path('sport/search/', SportsViews.search, name='search'),
    path('register/',views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('all-users/', views.all_users, name='all_users'),
    path('create-user/', views.create_user, name='create_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('view-users/', views.view_users, name='view_users'),
    path('add-friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('send-message/<int:user_id>/', views.send_message, name='send_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'sport_connect.views.custom_404_view'