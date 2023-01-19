from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.Signup.as_view()),
    path('login/', views.Login.as_view()),
    path('breaktimes/', views.Breaktime.as_view()),
    path('details/', views.Detail.as_view()),
    path('waitings/', views.Waitings.as_view()),
    path('cancellations/', views.Cancellations.as_view()),
    path('notifications/', views.Enter_notify.as_view()),
    path('search/', views.search),
]
