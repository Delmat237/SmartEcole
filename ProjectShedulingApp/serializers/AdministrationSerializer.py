from rest_framework import serializers
from ProjectShedulingApp.models import MembreAdmin, AdministrativeService

class AdministrativeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeService
        fields = ['id', 'name', 'type', 'description']

class MembreAdminSerializer(serializers.ModelSerializer):
    administrative_service = AdministrativeServiceSerializer(read_only=True)
    administrative_service_id = serializers.PrimaryKeyRelatedField(
        queryset=AdministrativeService.objects.all(), source='administrative_service', write_only=True
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MembreAdmin
        fields = ['id', 'name', 'type', 'poste', 'administrative_service', 'administrative_service_id', 'password','role']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        membre_admin = super().create(validated_data)
        if password:
            membre_admin.set_password(password)  # Assurez-vous que la méthode `set_password` est disponible
            membre_admin.save()
        return membre_admin

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
