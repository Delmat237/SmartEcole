from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ProjectShedulingApp.serializers.AdminSerializer import LoginMembreAdminSerializer, AdministrativeServiceSerializer, MembreAdminSerializer
from ProjectShedulingApp.models import MembreAdmin, AdministrativeService
from rest_framework import status

class AdministrativeServiceViewSet(viewsets.ModelViewSet):
    queryset = AdministrativeService.objects.all()
    serializer_class = AdministrativeServiceSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        try :
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response({
                'success': True,
                'message': 'Liste des services administratifs récupérée avec succès',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)  #
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Erreur lors de la récupération des services administratifs',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Service administratif récupéré avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class MembreAdminViewSet(viewsets.ModelViewSet):
    queryset = MembreAdmin.objects.all()
    serializer_class = MembreAdminSerializer

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
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'success': True,
                'message': 'Membre administratif créé avec succès',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({
                'success': False,
                'message': 'Erreur lors de la création du membre administratif',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginMembreAdminAPIView(APIView):
    """
    API pour se connecter avec email et mot de passe.
    """
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
            user = MembreAdmin.validated_data
            
            
 
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
                'message': "Données invalides",
                'error': e.detail.get('non_field_errors', ["Erreur inconnue"])[0]
            }, status=status.HTTP_400_BAD_REQUEST)