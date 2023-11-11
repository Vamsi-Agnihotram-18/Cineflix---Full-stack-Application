from account.serializers import SignUpSerializer, LoginSerializer
from account.auth import APIAccessAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Token


class UserSignUpAPI(APIView):
    InputSerializer = SignUpSerializer

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Token.objects.get_or_create(user=user)
        return Response(
            {
                "success": True,
                "token": APIAccessAuthentication.generate_jwt_token(user),
                "email": user.email,
                "role": user.role,
                "username": user.username,
                "phoneNumber": str(user.phoneNumber),
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginAPI(APIView):
    InputSerializer = LoginSerializer

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "success": True,
                "token": APIAccessAuthentication.generate_jwt_token(serializer.validated_data["user"]),
                "email": serializer.validated_data["user"].email,
                "role": serializer.validated_data["user"].role,
                "username": serializer.validated_data["user"].username,
                "phoneNumber": str(serializer.validated_data["user"].phoneNumber),
            },
            status=status.HTTP_200_OK,
        )
