from ProjectShedulingApp.models import Teacher
from ProjectShedulingApp.serializers.PersonSerializer import TeacherSerializer,LoginTeacherSerializer,LoginMembreAdminSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated
from rest_framework import viewsets
from drf_yasg import openapi
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from ProjectShedulingApp.models import CustomUser, Student,Teacher,Department

def create_teacher(matricule, phone_number, department, password):
    # 🔥 Créer le CustomUser lié
    user = CustomUser.objects.create(username=matricule, user_type="student")
    user.set_password(password)  # 🔐 Hash du mot de passe
    user.save()
    try:
        department_instance = Department.objects.get(id=department)  # 🔥 Convertir l'ID en instance
    except Department.DoesNotExist:
        raise ValueError("Département invalide")  # 🔥 Gérer l'erreur si l'ID est incorrect

    # 🔥 Créer le Student associé
    teacher = Teacher.objects.create(
        user=user,
        matricule=matricule,
        phone_number=phone_number,
        department=department_instance
    )
    return teacher
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'message': 'Liste des personnes récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Personne récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        matricule = request.data.get("matricule")
        
        phone_number = request.data.get("phone_number")
        department = request.data.get("department")
        password = request.data.get("password")

        try:
            student = create_teacher(matricule,phone_number, department, password)  # 🔥 Création via la fonction utilitaire

            serializer = TeacherSerializer(student)  # Sérialisation de l'objet créé
            return Response({
                'success': True,
                'message': 'Étudiant créé avec succès',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)  # Correction ici : `status.HTTP_201_CREATED`
        except ValueError as e: 
            return Response({
                'success': False,
                'message': 'Erreur lors de la création de l\'étudiant',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Personne modifiée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Personne supprimée avec succès',
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)



class LoginTeacherAPIView(APIView):
    """
    API pour se connecter avec email et mot de passe.
    """
    permission_classes = [AllowAny]
    @extend_schema(
        request=LoginTeacherSerializer,
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