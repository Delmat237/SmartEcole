from django.contrib import admin
from django.contrib import admin
from .models import CustomUser, Student, Teacher, Department, Requete

admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Requete)



# Register your models here.
