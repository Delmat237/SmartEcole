from rest_framework import viewsets, status
from rest_framework.response import Response
from ProjectShedulingApp.models import Requete
from ProjectShedulingApp.serializers.RequeteSerializer import RequeteSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class RequeteViewSet(viewsets.ModelViewSet):
    queryset = Requete.objects.all()
    serializer_class = RequeteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Requête créée avec succès',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Erreur lors de la création',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Liste des requêtes',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
