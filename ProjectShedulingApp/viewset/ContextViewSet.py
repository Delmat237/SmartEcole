from rest_framework import viewsets, status
from rest_framework.response import Response
from ProjectShedulingApp.models import AdministrativeService, Department, Requete, Reservation
from ProjectShedulingApp.serializers.DepartmentSerializer import DepartmentSerializer
from ProjectShedulingApp.serializers.AdministrationSerializer import AdministrativeServiceSerializer
from rest_framework.permissions import AllowAny

class ContextViewSet(viewsets.ViewSet):
    """
    ViewSet pour récupérer le contexte (ex: départements et services administratifs).
    """
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """
        Liste les départements et services administratifs avec une réponse formatée.
        """
        departments = Department.objects.all()
        admin_services = AdministrativeService.objects.all()

        department_serializer = DepartmentSerializer(departments, many=True)
        admin_service_serializer = AdministrativeServiceSerializer(admin_services, many=True)

        total_requests_sent = 0
        total_requests_received = 0
        total_reservations = 0

        user = request.user
        if user.is_authenticated:
            if user.user_type == "student":
                total_requests_sent = Requete.objects.filter(sender=user).count()
                total_reservations = Reservation.objects.filter(student=user).count()
            elif user.user_type in ["teacher", "admin"]:
                total_requests_sent = Requete.objects.filter(sender=user).count()
                total_requests_received = Requete.objects.filter(receiver=user).count()
                total_reservations = Reservation.objects.filter(submitter=user).count()

        return Response({
            'success': True,
            'message': 'Liste des catégories récupérée avec succès',
            'data': {
                "total": {
                    "total_requests_sent": total_requests_sent,
                    "total_requests_received": total_requests_received,
                    "total_reservations": total_reservations
                },
                "department": department_serializer.data,
                "administrative_service": admin_service_serializer.data
            }
        }, status=status.HTTP_200_OK)
