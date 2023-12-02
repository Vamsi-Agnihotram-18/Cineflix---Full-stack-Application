from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from account.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from core.errors import InvalidRequestError

INVALID_CRED_TXT = "Invalid Credentials"

class CustomSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    is_admin = serializers.BooleanField(required=False)

    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    username = serializers.CharField(max_length=24, required=False)
    phoneNumber = PhoneNumberField()

    class Meta:
        model = User
        fields = ("id", "email", "password", "confirm_password", "username", "phoneNumber", "role", "is_admin")

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if attrs["email"].endswith("@movieflix.com"):
            attrs["is_admin"] = True
        else:
            attrs["is_admin"] = False
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
            validated_data.get("username"),
            validated_data["phoneNumber"],
            validated_data["role"],
            validated_data["is_admin"]
        )
        return user


class CustomLoginSerializer(serializers.Serializer):
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


class CustomUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    username = serializers.CharField(max_length=24, required=False)
    phoneNumber = PhoneNumberField()
    # Add other fields from your User model if needed
