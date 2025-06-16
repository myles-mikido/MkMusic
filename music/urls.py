from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('download-options/<int:music_id>/', views.download_options, name='download_options'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('FAQ/', views.FAQ, name='FAQ'),
    path('download-multiple/', views.download_multiple, name='download_multiple'),

]