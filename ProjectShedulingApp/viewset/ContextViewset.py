
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ProjectShedulingApp.models import Requete, Reservation, CustomUser
from rest_framework.permissions import AllowAny

class ContextViewset(APIView):
    permission_classes = [IsAuthenticated]  # Sécurité : accès réservé aux utilisateurs connecté
    def get(self, request):
        user = request.user  # 🔥 Récupérer l'utilisateur actuel
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

        return Response({
            "success": True,
            "message": "Statistiques récupérées avec succès",
            "data": stats
        }, status=200)
