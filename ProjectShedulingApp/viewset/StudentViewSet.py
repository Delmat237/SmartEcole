from rest_framework import viewsets, status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from rest_framework.response import Response
from ProjectShedulingApp.models import Student
from ProjectShedulingApp.serializers.LoginSerializer import LoginStudentSerializer
from ProjectShedulingApp.serializers.PersonSerializer import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'message': 'Liste des étudiants récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Étudiant récupéré avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Étudiant créé avec succès',
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
            'message': 'Étudiant modifié avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Étudiant supprimé avec succès',
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)


class LoginStudentAPIView(APIView):
    """
    API pour se connecter avec email et mot de passe.
    """
    serializer_class = LoginStudentSerializer
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
            user = serializer.validated_data  # L'utilisateur authentifié
            # Générer ou récupérer le token associé à cet utilisateur
            token, created = Token.objects.get_or_create(user=user)
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
