from django.urls import path
from . import views


urlpatterns = [
    path('', views.Waitings.as_view()),
    path('my/', views.WaitingsMy.as_view())
]
