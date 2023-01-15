from django.urls import path
from . import views


urlpatterns = [
    path('signin/', views.Signin.as_view()),
    path('breaktime/', views.Breaktime.as_view()),
    path('detail/', views.Detail.as_view()),
    path('waitings/', views.Waitings.as_view()),
    path('cancellations/', views.Cancellations.as_view()),
    path('notifications/', views.Enter_notify.as_view()),
]
