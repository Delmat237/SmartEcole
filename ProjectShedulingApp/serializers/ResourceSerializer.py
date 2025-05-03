from ProjectShedulingApp.models import SalleDeClasse, Ordinateur, VideoProjecteur
from rest_framework import serializers


class MaterielPedagogiqueSerializer(serializers.Serializer):
    nom = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True)
    categorie = serializers.CharField(max_length=50)
    disponible = serializers.BooleanField(default=True)


class OrdinateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordinateur
        fields = [
            'id',
            'nom',
            'description',
            'categorie',
            'disponible',
            'adresse_mac',
            'processeur',
            'ram',
            'stockage'
        ]

class VideoProjecteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProjecteur
        fields = [
            'id',
            'nom',
            'description',
            'categorie',
            'disponible',
            'resolution',
            'connectivite',
            'luminosite'
        ]


class SalleDeClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalleDeClasse
        fields = [
            'id',
            'nom',
            'description',
            'categorie',
            'disponible',
            'capacite',
            'numero_salle'
        ]
