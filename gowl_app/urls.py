from django.urls import path

from gowl_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('spreadsheet', views.user_spreadsheet, name='user_spreadsheet'),
    path('profile', views.user_profile, name='user_profile'),
    path('@<str:username>/', views.user_gowl, name='user_gowl'),
    path('law/privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('law/tos', views.terms_of_service, name='terms_of_service')
]
