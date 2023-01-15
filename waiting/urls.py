from django.urls import path
from . import views


urlpatterns = [
    path('', views.Waitings.as_view()),
    path('My/', views.WaitingsMy.as_view())
]
