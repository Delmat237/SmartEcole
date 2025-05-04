from rest_framework import serializers
from ProjectShedulingApp.models import Requete

class RequeteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requete
        fields = '__all__'
