from rest_framework import viewsets
from ProjectShedulingApp.models import Ordinateur
from rest_framework.response import Response
from rest_framework import status

from ProjectShedulingApp.serializers.ResourceSerializer import OrdinateurSerializer

class OrdinateurViewSet (viewsets.ModelViewSet):
    queryset = Ordinateur.objects.all()
    serializer_class = OrdinateurSerializer
    

    def list(self, request, *args, **kwargs):
        # Custom handling of the 'list' action
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'message': 'Liste des Ordinateurs récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        # Custom handling of the 'retrieve' action
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Ordinateurs récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
