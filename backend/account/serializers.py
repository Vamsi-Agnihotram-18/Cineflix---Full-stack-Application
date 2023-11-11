from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from account.models import User
from phonenumber_field.serializerfields import PhoneNumberField

INVALID_CRED_TXT = "Invalid Credentials"


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    username = serializers.CharField(max_length=24, required=False)
    phoneNumber = PhoneNumberField()

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password", "username", "phoneNumber", "role")

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
            validated_data["username"],
            validated_data["phoneNumber"],
            validated_data["role"],
        )
        return user

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data["phoneNumber"] = str(instance.phoneNumber)
    #     return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        try:
            user = None
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise AuthenticationFailed(INVALID_CRED_TXT)

        attrs["user"] = user

        if not user.check_password(attrs["password"]):
            raise AuthenticationFailed(INVALID_CRED_TXT)

        return attrs
