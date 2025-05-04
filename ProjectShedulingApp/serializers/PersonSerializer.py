from ProjectShedulingApp.models import  Student, Teacher, MembreAdmin,CustomUser
from rest_framework import serializers
from ProjectShedulingApp.models import CustomUser, Student

def create_student(matricule, email, phone_number, niveau, password):
    # 🔥 Créer le CustomUser lié
    user = CustomUser.objects.create(username=matricule, user_type="student")
    user.set_password(password)  # 🔐 Hash du mot de passe
    user.save()

    # 🔥 Créer le Student associé
    student = Student.objects.create(
        user=user,
        matricule=matricule,
        email=email,
        phone_number=phone_number,
        niveau=niveau
    )

    return student


'''class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'matricule', 'email', 'phoneNumber']
'''
class CustomUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        #fields = ['id', 'name', 'matricule', 'email', 'phoneNumber', 'first_name', 'last_name']
        fields = '__all__'

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        #fields = '__all__'
        exclude = ['user']

    def create(self, validated_data):
        # Création automatique d'un utilisateur CustomUser
        user = CustomUser.objects.create(username=validated_data["matricule"], user_type="student")
        student = Student.objects.create(user=user, **validated_data)
        return student

class TeacherSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Teacher
        exclude = ['user']
    def create(self, validated_data):
        # Création automatique d'un utilisateur CustomUser
        user = CustomUser.objects.create(username=validated_data["matricule"], user_type="teacher")
        student = Teacher.objects.create(user=user, **validated_data)
        return student

    
    def create(self, validated_data):
        # Création automatique d'un utilisateur CustomUser
        user = CustomUser.objects.create(username=validated_data["matricule"], user_type="student")
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher


class MembreAdminSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'administrative_service', 'user','first_name','last_name']

        
# Serializer pour la connexion (login)
'''
class LoginStudentSerializer(serializers.Serializer):
    matricule = serializers.CharField()  # Remplacement d'email par matricule
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        matricule = data.get("matricule")
        password = data.get("password")

        try:
            user = Student.objects.get(matricule=matricule)  # Correction du champ
        except Student.DoesNotExist:
            raise serializers.ValidationError("Matricule ou mot de passe invalide")

        if not user.check_password(password):
            raise serializers.ValidationError("Matricule ou mot de passe invalide")

        if not user.is_active:
            raise serializers.ValidationError("Informations invalides.")

        return user
'''

class LoginStudentSerializer(serializers.Serializer):
    matricule = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        matricule = data.get("matricule")
        password = data.get("password")

        try:
            student = Student.objects.get(matricule=matricule)  # Trouver le Student
            user = student.user  #  Obtenir le CustomUser lié
        except Student.DoesNotExist:
            raise serializers.ValidationError("Matricule ou mot de passe invalide")

        if not user or not user.check_password(password):  #  Vérification via CustomUser
            raise serializers.ValidationError("Matricule ou mot de passe invalide")

        if not user.is_active:
            raise serializers.ValidationError("Compte inactif.")

        return user  # Retourner CustomUser

class LoginTeacherSerializer(serializers.Serializer):
    matricule = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        matricule = data.get("matricule")
        password = data.get("password")

        try:
            teacher = Teacher.objects.get(matricule=matricule)  # Trouver le Student
            user = teacher.user  #  Obtenir le CustomUser lié
        except Teacher.DoesNotExist:
            raise serializers.ValidationError("Matricule ou mot de passe invalide")

        if not user or not user.check_password(password):  #  Vérification via CustomUser
            raise serializers.ValidationError("Matricule ou mot de passe invalide")

        if not user.is_active:
            raise serializers.ValidationError("Compte inactif.")

        return user  # Retourner CustomUser



class LoginMembreAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # Méthode de validation pour vérifier que les identifiants sont corrects
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = MembreAdmin.objects.get(email=email)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Email ou mot de passe invalide")

        if not user.check_password(password):
            raise serializers.ValidationError("Email ou mot de passe invalide")

        if not user.is_active:
            raise serializers.ValidationError("Informations invalide.")

        return user