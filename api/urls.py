from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view()),
    # path("booking", BookingView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
