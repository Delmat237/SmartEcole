from rest_framework import serializers

class StatsSerializer(serializers.Serializer):
    total_requests_sent = serializers.IntegerField()
    total_requests_received = serializers.IntegerField()
    total_reservations = serializers.IntegerField()
