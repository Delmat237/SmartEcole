from rest_framework import viewsets
from ProjectShedulingApp.models import SalleDeClasse
from rest_framework.response import Response
from rest_framework import status

from ProjectShedulingApp.serializers.ResourceSerializer import SalleDeClasseSerializer

class SalleDeClasseViewSet (viewsets.ModelViewSet):
    queryset = SalleDeClasse.objects.all()
    serializer_class = SalleDeClasseSerializer
    

    def list(self, request, *args, **kwargs):
        # Custom handling of the 'list' action
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'message': 'Liste des SalleDeClasse récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        # Custom handling of the 'retrieve' action
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'SalleDeClasse récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
