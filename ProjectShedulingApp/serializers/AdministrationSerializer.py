from ProjectShedulingApp.models import AdministrativeService, MembreAdmin
from rest_framework import serializers

class AdministrativeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeService
        fields = ['id', 'name', 'type', 'description']

class MembreAdminSerializer(serializers.ModelSerializer):
    administrative_service = AdministrativeServiceSerializer(read_only=True)
    administrative_service_id = serializers.PrimaryKeyRelatedField(
        queryset=AdministrativeService.objects.all(), source='administrative_service', write_only=True
    )

    class Meta:
        model = MembreAdmin
        fields = ['id', 'name', 'type', 'poste', 'administrative_service', 'administrative_service_id']
