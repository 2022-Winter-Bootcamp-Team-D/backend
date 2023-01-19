from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import SignupAPIView, SigninView

urlpatterns = [
    path("signup/", SignupAPIView.as_view()),
    path("signin/", SigninView.as_view()),
    path('refresh/', TokenRefreshView.as_view()), # access_token 재발급하기
]
