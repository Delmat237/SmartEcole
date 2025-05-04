from ProjectShedulingApp.models import MaterielPedagogique
from ProjectShedulingApp.serializers import ResourceSerializer
from rest_framework import viewsets



from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from ProjectShedulingApp.models  import ClassRoom
from ProjectShedulingApp.serializers.ResourceSerializer import ClassRoomSerializer
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = MaterielPedagogique.objects.all()
    serializer_class = ResourceSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'success': True,
            'message': 'Liste des ressources récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Ressource récupérée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'message': 'Ressource créée avec succès',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'message': 'Ressource modifiée avec succès',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'message': 'Ressource supprimée avec succès',
            'data': None
        }, status=status.HTTP_204_NO_CONTENT)



class ClassRoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les salles de classe avec réponses personnalisées
    """
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'building', 'room_number']
    ordering_fields = ['name', 'capacity', 'building', 'floor']
    
    def get_response_data(self, data, message=None, success=True, status_code=status.HTTP_200_OK):
        """Structure standard pour les réponses JSON"""
        return {
            "success": success,
            "status_code": status_code,
            "message": message,
            "data": data
        }

    def list(self, request, *args, **kwargs):
        """Liste des salles de classe avec réponse personnalisée"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                self.get_response_data(serializer.data, "Liste des salles récupérée avec succès")
            )
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            self.get_response_data(serializer.data, "Liste des salles récupérée avec succès")
        )

    def create(self, request, *args, **kwargs):
        """Création d'une salle de classe avec réponse personnalisée"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                self.get_response_data(serializer.data, "Salle créée avec succès", status_code=status.HTTP_201_CREATED),
                status=status.HTTP_201_CREATED
            )
        return Response(
            self.get_response_data(serializer.errors, "Erreur lors de la création", False, status.HTTP_400_BAD_REQUEST),
            status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, *args, **kwargs):
        """Détails d'une salle de classe avec réponse personnalisée"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            self.get_response_data(serializer.data, "Détails de la salle récupérés avec succès")
        )

    def update(self, request, *args, **kwargs):
        """Mise à jour complète d'une salle de classe avec réponse personnalisée"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                self.get_response_data(serializer.data, "Salle mise à jour avec succès")
            )
            
        return Response(
            self.get_response_data(serializer.errors, "Erreur lors de la mise à jour", False, status.HTTP_400_BAD_REQUEST),
            status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, *args, **kwargs):
        """Mise à jour partielle d'une salle de classe"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Suppression d'une salle de classe avec réponse personnalisée"""
        instance = self.get_object()
        instance.delete()
        return Response(
            self.get_response_data({}, "Salle supprimée avec succès", status_code=status.HTTP_204_NO_CONTENT),
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Action personnalisée pour obtenir des détails étendus"""
        classroom = self.get_object()
        serializer = self.get_serializer(classroom)
        
        # Vous pouvez ajouter des données supplémentaires ici
        extended_data = {
            **serializer.data,
            "additional_info": {
                "reservations_count": classroom.reservations.count(),
                "is_available": classroom.is_available_now(),
                # Ajoutez d'autres champs personnalisés selon vos besoins
            }
        }
        
        return Response(
            self.get_response_data(extended_data, "Détails étendus récupérés avec succès")
        )
    
    @staticmethod
    def generate_request_pdf(request_obj):
        """Génère un PDF pour une requête (conservé depuis votre version originale)"""
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # ... (le reste de votre méthode generate_request_pdf)
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
    
    @staticmethod
    def generate_reservation_pdf(reservation_obj):
        """Génère un PDF pour une réservation (conservé depuis votre version originale)"""
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # ... (le reste de votre méthode generate_reservation_pdf)
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer