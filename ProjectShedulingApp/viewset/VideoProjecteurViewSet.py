from rest_framework import viewsets
from ProjectShedulingApp.models import VideoProjecteur
from rest_framework.response import Response
from rest_framework import status

from ProjectShedulingApp.serializers.ResourceSerializer import VideoProjecteurSerializer

class VideoProjecteurViewSet (viewsets.ModelViewSet):
    queryset = VideoProjecteur.objects.all()
    serializer_class = VideoProjecteurSerializer
    

    def list(self, request, *args, **kwargs):
        # Custom handling of the 'list' action
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'message': 'Liste des Video projecteur récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        # Custom handling of the 'retrieve' action
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Video projecteur récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
