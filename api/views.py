from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    AuthenticationFailed,
)
from .serializers import UserSerializer
from .models import User
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found.")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password.")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response()
        response.set_cookie(key="jwt", value=access_token, httponly=True)

        response.data = {"refresh": str(refresh)}

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}

        return response


# class BookingView(APIView):
#     def get(self, request):
#         token = request.COOKIES.get("jwt")

#         if not token:
#             raise AuthenticationFailed("Unauthenticated")

#         try:
#             payload = jwt.decode(token, secret, algorithms=["HS256"])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Token expired!!")

#         user = User.objects.filter(id=payload["id"]).first()
#         serializer = BookingSerializer(user)

#         return Response(serializer.data)

#     def post(self, request):
#         token = request.COOKIES.get("jwt")

#         if not token:
#             raise AuthenticationFailed("Login first!!")

#         try:
#             payload = jwt.decode(token, secret, algorithms=["HS256"])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Token expired!!")

#         serializer = BookingSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = User.objects.filter(id=payload["id"]).first()

#         if not user:
#             raise NotFound("User not found.")

#         serializer.save(user=user)

#         return Response(serializer.data)
