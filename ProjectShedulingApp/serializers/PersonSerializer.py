from ProjectShedulingApp.models import Student, Teacher
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from ProjectShedulingApp.serializers.LoginSerializer import LoginStudentSerializer
from ProjectShedulingApp.serializers.LoginSerializer import LoginTeacherSerializer


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'niveau', 'matricule', 'email', 'phone_number', 'first_name', 'last_name', 'password']

class TeacherSerializer(serializers.ModelSerializer):
    # Remplacez 'user' par les informations directement liées à l'enseignant
    class Meta:
        model = Teacher
        fields = ['id', 'department', 'matricule', 'email', 'phone_number', 'first_name', 'last_name', 'password']

class LoginStudentAPIView(APIView):
    """
    API pour se connecter avec email et mot de passe.
    """
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=LoginStudentSerializer,
        responses={
            200: openapi.Response(description="Connexion réussie"),
            400: openapi.Response(description="Échec de connexion"),
        }
    )
    def post(self, request):
        try:
            serializer = LoginStudentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'message': 'Connexion réussie',
                'data': {
                    'token': token.key,
                    'user': StudentSerializer(user).data
                }
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                'success': False,
                'message': "Connexion échouée",
                'error': e.detail.get('non_field_errors', ["Erreur inconnue"])[0]
            }, status=status.HTTP_400_BAD_REQUEST)
        
class LoginTeacherAPIView(APIView):
    """
    API pour se connecter avec email et mot de passe.
    """
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=LoginTeacherSerializer,
        responses={
            200: openapi.Response(description="Connexion réussie"),
            400: openapi.Response(description="Échec de connexion"),
        }
    )
    def post(self, request):
        try:
            serializer = LoginTeacherSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'message': 'Connexion réussie',
                'data': {
                    'token': token.key,
                    'user': TeacherSerializer(user).data
                }
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                'success': False,
                'message': "Connexion échouée",
                'error': e.detail.get('non_field_errors', ["Erreur inconnue"])[0]
            }, status=status.HTTP_400_BAD_REQUEST)