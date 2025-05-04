from rest_framework.response import Response
from rest_framework import viewsets, status
from ProjectShedulingApp.models import Department
from ProjectShedulingApp.serializers.DepartmentSerializer import DepartmentSerializer
from rest_framework.permissions import AllowAny

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]

    # Optionnel : vous pouvez redéfinir ces méthodes si vous avez besoin de personnalisation
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print("Queryset:", queryset)  # Affiche les objets récupérés depuis la base
        serializer = self.get_serializer(queryset, many=True)
        print("Serialized Data:", serializer.data)  # Affiche les données sérialisées
        return Response({
            'success': True,
            'message': 'Liste des départements récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Département récupéré avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
