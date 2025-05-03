from ProjectShedulingApp.models import CustomUser, Person, Student, Teacher
from rest_framework import serializers

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'matricule', 'email', 'phoneNumber']

class CustomUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'matricule', 'email', 'phoneNumber', 'first_name', 'last_name']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'niveau', 'user']


class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'department', 'user']

