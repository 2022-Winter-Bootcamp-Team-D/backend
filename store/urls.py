from django.urls import path
from . import views


urlpatterns = [
    path('signin/', views.signin),
    path('breaktime/', views.breaktime),
]
