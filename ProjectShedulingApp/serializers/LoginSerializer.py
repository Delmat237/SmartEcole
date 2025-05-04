from rest_framework import serializers
from ProjectShedulingApp.models import Student, Teacher
from django.contrib.auth import authenticate


class LoginStudentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        student = authenticate(email=data['email'], password=data['password'])
        if student is None:
            raise serializers.ValidationError("Email ou mot de passe incorrect")

        return student


class LoginTeacherSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        teacher = authenticate(email=data['email'], password=data['password'])
        if teacher is None:
            raise serializers.ValidationError("Email ou mot de passe incorrect")

        return teacher