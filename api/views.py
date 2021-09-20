from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    AuthenticationFailed,
    ValidationError,
    PermissionDenied,
    NotFound,
)
from .serializers import UserSerializer, BookingSerializer
from .models import User, Booking
import jwt, datetime


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found.")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password.")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        # secret should be in the prod env, not here
        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)

        response.data = {"jwt": token}

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired!!")

        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}

        return response


class BookingView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired!!")

        user = User.objects.filter(email=payload["email"]).first()
        serializer = BookingSerializer(user)

        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user:
            raise PermissionDenied("Provide user!!")

        if not request.data.get("email"):
            raise ValidationError("Email must be provided.")

        user = User.objects.filter(email=request.data["email"]).first()
        if not user:
            raise NotFound("User not found.")

        serializer.save(user=user)

        return Response(serializer.data)
