from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from ProjectShedulingApp.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = Reservation
        fields = '__all__'
