from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_spectacular.utils import extend_schema
from ProjectShedulingApp.models import Student
from rest_framework.authtoken.models import Token
from ProjectShedulingApp.serializers.PersonSerializer import StudentSerializer, LoginStudentSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated
from ProjectShedulingApp.models import CustomUser, Student,Teacher

def create_student(matricule, email, phone_number, niveau, password):
    # 🔥 Créer le CustomUser lié
    user = CustomUser.objects.create(username=matricule, user_type="student")
    user.set_password(password)  # 🔐 Hash du mot de passe
    user.save()

    try:
    # 🔥 Créer le Student associé
        student = Student.objects.create(
            user=user,
            matricule=matricule,
            email=email,
            phone_number=phone_number,
            
        )

        return student
    except Exception as e:
        # Si l'utilisateur existe déjà, on lève une exception
        raise ValidationError("L'utilisateur existe déjà avec ce matricule ou email.")



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
        matricule = request.data.get("matricule")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        niveau = request.data.get("niveau")
        password = request.data.get("password")
        try:
                student = create_student(matricule, email, phone_number, niveau, password)  # 🔥 Création via la fonction utilitaire

                serializer = StudentSerializer(student)  # Sérialisation de l'objet créé
                return Response({
                    'success': True,
                    'message': 'Étudiant créé avec succès',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)  # Correction ici : `status.HTTP_201_CREATED`
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Erreur lors de la création de l\'étudiant',
                'error': "Matricule ou email déjà utilisé"
            }, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = [AllowAny]
    @extend_schema(
        request=LoginStudentSerializer,

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
