from rest_framework import serializers
from ProjectShedulingApp.models import CategoryResource

class CategoryResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryResource
        fields = ['id', 'name', 'description']
