# from django.shortcuts import render
# from django.core.mail import send_mail
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from rest_framework_simplejwt.tokens import RefreshToken

# from .models import CustomUser
# from .serializers import RegisterSerializer, LoginSerializer

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()

#             send_mail(
#                 subject='أهلاً وسهلاً بك!',
#                 message=f'مرحباً {user.name}!\nنحن سعداء بانضمامك إلينا.',
#                 from_email='no-reply@example.com',
#                 recipient_list=[user.email],
#                 fail_silently=False,
#             )

#             return Response({"message": "User registered successfully"}, status=201)
#         return Response(serializer.errors, status=400)


# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         return Response(serializer.errors, status=400)


# class ProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         return Response({
#             "id": user.id,
#             "email": user.email,
#             "name": user.name
#         })


from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Optional: send welcome email
            send_mail(
                subject='أهلاً وسهلاً بك!',
                message=f'مرحباً {user.name}!\nنحن سعداء بانضمامك إلينا.',
                from_email='no-reply@example.com',
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "name": user.name
        }, status=status.HTTP_200_OK)
