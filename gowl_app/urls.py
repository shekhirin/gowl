from django.urls import path

from gowl_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('spreadsheet', views.user_spreadsheet, name='user_spreadsheet'),
    path('profile', views.user_profile, name='user_profile'),
    path('@<str:username>/', views.user_gowl, name='user_gowl')
]
