from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from ProjectShedulingApp.models import MembreAdmin
from ProjectShedulingApp.serializers.AdminSerializer import LoginMembreAdminSerializer, MembreAdminSerializer
from ProjectShedulingApp.permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from drf_yasg import openapi

class MembreAdminViewSet(viewsets.ModelViewSet):
    queryset = MembreAdmin.objects.all()
    serializer_class = MembreAdminSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'message': 'Liste des membres administratifs récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Membre administratif récupéré avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class LoginMembreAdminAPIView(APIView):
    """
    API pour se connecter avec email et mot de passe.
    """
    serializer_class = LoginMembreAdminSerializer
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=LoginMembreAdminSerializer,
        responses={
            200: openapi.Response(description="Connexion réussie"),
            400: openapi.Response(description="Échec de connexion"),
        }
    )
    def post(self, request):
        try:
            serializer = LoginMembreAdminSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'message': 'Connexion réussie',
                'data': {
                    'token': token.key,
                    'user': LoginMembreAdminSerializer(user).data
                }
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({
                'success': False,
                'message': "Connexion échouée",
                'error': e.detail.get('non_field_errors', ["Erreur inconnue"])[0]
            }, status=status.HTTP_400_BAD_REQUEST)