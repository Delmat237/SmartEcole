from rest_framework import serializers
from ProjectShedulingApp.models import MembreAdmin, AdministrativeService, CustomUser

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
        fields = ['id', 'user', 'name', 'type', 'poste', 'administrative_service', 'administrative_service_id']
