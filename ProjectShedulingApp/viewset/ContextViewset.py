
"""from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from ProjectShedulingApp.models import Requete, Reservation, CustomUser
from ProjectShedulingApp.serializers.StatsSerializer import StatsSerializer  # Assurez-vous que le sérialiseur est bien importé

class ContextViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]  # Accès réservé aux utilisateurs authentifiés
    serializer_class = StatsSerializer  # Ajouter le sérialiseur ici

    @action(detail=False, methods=['get'])
    def get_stats(self, request):  # Renommé pour plus de clarté
        user = request.user  # Récupérer l'utilisateur actuel depuis la requête
        stats = {
            "total_requests_sent": 0,
            "total_requests_received": 0,
            "total_reservations": 0
        }

        if user.user_type == "student":
            stats["total_requests_sent"] = Requete.objects.filter(sender=user).count()
            stats["total_reservations"] = Reservation.objects.filter(student=user).count()

        elif user.user_type == "teacher" or user.user_type == "admin":
            stats["total_requests_sent"] = Requete.objects.filter(sender=user).count()
            stats["total_requests_received"] = Requete.objects.filter(receiver=user).count()
            stats["total_reservations"] = Reservation.objects.filter(submitter=user).count()

        # Sérialiser les statistiques avant de les renvoyer
        serializer = StatsSerializer(stats)
        return Response({
            "success": True,
            "message": "Statistiques récupérées avec succès",
            "data": serializer.data  # Renvoi des données sérialisées
        }, status=200)
"""