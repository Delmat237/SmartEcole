

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from ProjectShedulingApp.models import Service
from ProjectShedulingApp.serializers.DepartmentSerializer import ServiceSerializer
import io

from PIL import Image
import json



class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les services
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="Liste des services récupérée avec succès"
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            data=serializer.data,
            message="Détails du service récupérés avec succès"
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse.success(
                data=serializer.data,
                message="Service créé avec succès",
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.error(
            message="Erreur lors de la création du service",
            errors=serializer.errors
        )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            return CustomResponse.success(
                data=serializer.data,
                message="Service mis à jour avec succès"
            )
        return CustomResponse.error(
            message="Erreur lors de la mise à jour du service",
            errors=serializer.errors
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CustomResponse.success(
            message="Service supprimé avec succès",
            status_code=status.HTTP_204_NO_CONTENT
        )

