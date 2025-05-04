from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ProjectShedulingApp.models import Reservation, Ordinateur
from ProjectShedulingApp.serializers.ReservationSerializer import ReservationSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


    def list(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'message': 'Liste des réservations récupérée avec succès',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        ordinateur = Ordinateur.objects.get(id=data['ordinateur'])
        # Vérifie la disponibilité ou les conflits de date ici (facultatif)

        self.perform_create(serializer)

        return Response({
            'success': True,
            'message': 'Réservation créée avec succès',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response({'message': "Modification non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"error": "Action non autorisée"}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Réservation annulée avec succès'
        }, status=status.HTTP_204_NO_CONTENT)
