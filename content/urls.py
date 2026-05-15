from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sira/', views.sira, name='sira'),
    path('riyad-useimin/', views.riyad_useimin, name='riyad_useimin'),
]