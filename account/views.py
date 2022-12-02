from rest_framework.response import Response
from rest_framework import status, filters, viewsets
from django.core.mail import send_mail  # for email
from django.shortcuts import get_object_or_404
from .serializers import (
    UserAccountVerificationSerializer,
    UserCreationSerializer,
    loginSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

# from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny


class AuthViewSets(viewsets.ModelViewSet):

    """User ViewSets"""

    queryset = get_user_model().objects.all()
    serializer_class = UserCreationSerializer  # default serializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    permission_classes = [AllowAny]
    http_method_names = ["get", "post", "patch", "delete", "put"]
    filterset_fields = ["is_active"]
    search_fields = ["email", "username", "first_name", "last_name", "phone_number"]
    ordering_fields = ["-date_joined"]

    def get_serializer_class(self):
        if self.action == "activate_account":
            return UserAccountVerificationSerializer
        elif self.action == "login_user":
            return loginSerializer
        elif self.action == "create":
            return UserCreationSerializer
        return super().get_serializer_class()

    def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        username = request.data["username"]
        reciever_email = request.data["email"].lower().strip()

        if serializer.is_valid():

            serializer.save()

            token = serializer.data["token"]

            body = f"Hi {username},\n You are seeing this message because you registered for Ebookify . Copy the code code below to verify your account   \n {token}"

            send_mail(
                "Confirmation code for account verification",
                body,
                "Ebookify.app.com",
                [reciever_email],
                fail_silently=False,
            )

            return Response(
                {
                    "success": True,
                    "message": "Account created successfully , check your email to continue the verification process ",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"success": False, "error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=["PUT"],
        detail=False,
        serializer_class=UserAccountVerificationSerializer,
        url_path="activate-account",
        url_name="activate_account",
    )
    def activate_account(self, request, *args, **kwargs):

        """This end point verifies ,activates the account if the token  sent to client email is matched with the database  thus setting the user field  {is_verified =True}"""

        user = get_object_or_404(User, email=request.data["email"])

        if user.token == request.data["token"]:

            user.is_verified = True
            user.save()

            serializer = self.serializer_class(instance=user)
            return Response(
                {"succes": True, "data": serializer.data}, status=status.HTTP_200_OK
            )

        return Response(
            data={"success": False, "message": "verification failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=["POST"],
        permission_classes=[AllowAny],
        detail=False,
        serializer_class=loginSerializer,
        url_path="login-user",
        url_name="login_user",
    )
    def login_user(self, request, *args, **kwargs):
        """User login and get the tokenpair of of access-token and refresh token"""

        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)

            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        user = User.objects.all().filter(email=request.data["email"]).first()
        if not user:
            return Response(
                data={"message": "Authentication Failed"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        passwordFlag = user.check_password(request.data["password"])

        if passwordFlag:

            if user.is_verified:

                tokens = get_tokens_for_user(user=user)
                serializer = self.serializer_class(instance=user)
                return Response(
                    data={"message": serializer.data, "token": tokens},
                    status=status.HTTP_200_OK,
                )

            return Response(
                data={"message": "Account not activated"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data={"message": "Authentication Failed"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
