from rest_framework import serializers
from ProjectShedulingApp.models import MaterielPedagogique, Ordinateur, VideoProjecteur, SalleDeClasse

class MaterielPedagogiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterielPedagogique
        fields = ['id', 'nom', 'description', 'categorie', 'disponible']

class OrdinateurSerializer(MaterielPedagogiqueSerializer):
    class Meta(MaterielPedagogiqueSerializer.Meta):
        model = Ordinateur
        fields = MaterielPedagogiqueSerializer.Meta.fields + ['adresse_mac', 'processeur', 'ram', 'stockage']

class VideoProjecteurSerializer(MaterielPedagogiqueSerializer):
    class Meta(MaterielPedagogiqueSerializer.Meta):
        model = VideoProjecteur
        fields = MaterielPedagogiqueSerializer.Meta.fields + ['resolution', 'connectivite', 'luminosite']

class SalleDeClasseSerializer(MaterielPedagogiqueSerializer):
    class Meta(MaterielPedagogiqueSerializer.Meta):
        model = SalleDeClasse
        fields = MaterielPedagogiqueSerializer.Meta.fields + ['capacite', 'numero_salle']
