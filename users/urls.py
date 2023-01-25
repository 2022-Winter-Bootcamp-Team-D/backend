from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import Signup, Signin

urlpatterns = [
    path("signup/", Signup.as_view()),
    path("signin/", Signin.as_view()),
    path('refresh/', TokenRefreshView.as_view()), # access_token 재발급하기
]
