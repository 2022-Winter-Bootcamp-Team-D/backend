from django.urls import path
from . import views


urlpatterns = [
    path('signin/', views.signin),
    path('breaktime/', views.breaktime),
    path('detail/', views.detail),
    path('waitings/', views.waitings),
    path('cancellations/', views.cancellations),
]
