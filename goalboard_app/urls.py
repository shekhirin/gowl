from django.urls import path

from goalboard_app import views

urlpatterns = [
    path('', views.home),
    path('spreadsheet', views.user_spreadsheet, name='user_spreadsheet'),
    path('profile', views.user_profile, name='user_profile'),
    path('@<str:username>/', views.user_goalboard, name='user_goalboard')
]
