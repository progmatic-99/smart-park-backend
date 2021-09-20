from .models import User, Booking
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        raw_password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if raw_password is not None:
            instance.set_password(raw_password)

        instance.save()
        return instance


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["slot_number", "cost", "time", "duration", "user_id"]
