from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, BookingView


urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("user", UserView.as_view()),
    path("logout", LogoutView.as_view()),
    path("booking", BookingView.as_view()),
]
