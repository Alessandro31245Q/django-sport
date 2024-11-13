
from . import views
from django.urls import path


urlpatterns = [
    path('<int:category_id>/', views.sport_by_category, name='sport_by_category'),
    path('sportsCategory/', views.sports_list, name='sports_list'),
    path('create-category/', views.create_category, name='create_category'),
    path('category/update/<int:category_id>/', views.update_category, name='update_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('courts/', views.court_list, name='court_list'),
    path('courts/create/', views.create_court, name='create_court'),
    path('courts/<int:court_id>/update/', views.update_court, name='update_court'),
    path('courts/<int:court_id>/delete/', views.delete_court, name='delete_court'),
]