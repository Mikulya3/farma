from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, \
    ForgotPasswordCompleteSerializer

User = get_user_model()

class RegisterUserAPIView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('you have successfully registered!', status=201)
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self,request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('password have successfully changed!')

class ActivationApiView(APIView):

    def get(self, request, activation_code):
            user = get_object_or_404(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'success'}, status=status.HTTP_200_OK)

class ForgotPasswordAPIView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('we have sent you letter to recovery your password!')


class ForgotPasswordCompleteAPIView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer)
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('password have successfully changed!')

