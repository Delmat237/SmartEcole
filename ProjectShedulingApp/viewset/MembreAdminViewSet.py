from rest_framework import viewsets, status
from rest_framework.response import Response
from ProjectShedulingApp.models import MembreAdmin
from ProjectShedulingApp.serializers.AdminSerializer import MembreAdminSerializer

class MembreAdminViewSet(viewsets.ModelViewSet):
    queryset = MembreAdmin.objects.all()
    serializer_class = MembreAdminSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'message': 'Liste des membres administratifs récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Membre administratif récupéré avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
