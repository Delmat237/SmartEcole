from ProjectShedulingApp.models import Teacher
from ProjectShedulingApp.serializers.LoginSerializer import LoginTeacherSerializer
from ProjectShedulingApp.serializers.PersonSerializer import TeacherSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'message': 'Liste des enseignants récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Enseignant récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Enseignant créée avec succès',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Enseignant modifiée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Enseignant supprimée avec succès',
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)

class LoginTeacherAPIView(APIView):
    """
    API pour se connecter avec email et mot de passe.
    """
    serializer_class = LoginTeacherSerializer
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