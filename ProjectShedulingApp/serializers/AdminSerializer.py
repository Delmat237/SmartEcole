from rest_framework import serializers
from ProjectShedulingApp.models import MembreAdmin, AdministrativeService

class AdministrativeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeService
        fields = '__all__'

class MembreAdminSerializer(serializers.ModelSerializer):
    administrative_service = AdministrativeServiceSerializer(read_only=True)
    administrative_service_id = serializers.PrimaryKeyRelatedField(
        queryset=AdministrativeService.objects.all(),
        source='administrative_service',
        write_only=True
    )

    class Meta:
        model = MembreAdmin
        fields = ['id', 'name', 'email','password','type', 'poste', 'administrative_service', 'administrative_service_id']

class LoginMembreAdminSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # Méthode de validation pour vérifier que les identifiants sont corrects
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = MembreAdmin.objects.get(email=email)
        except MembreAdmin.DoesNotExist:
            raise serializers.ValidationError("Email ou mot de passe invalide")

        if not user.check_password(password):
            raise serializers.ValidationError("Email ou mot de passe invalide")

        if not user.is_active:
            raise serializers.ValidationError("Informations invalide.")

        return user
