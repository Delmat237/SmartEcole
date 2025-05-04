from django.urls import include,path
from rest_framework.routers import DefaultRouter
from ProjectShedulingApp.viewset.StudentViewSet import LoginStudentAPIView
from ProjectShedulingApp.viewset.TeacherViewSet import LoginTeacherAPIView,LoginMembreAdminAPIView

from ProjectShedulingApp.viewset import StudentViewSet,TeacherViewSet,ResourceViewSet
from ProjectShedulingApp.viewset.servicesViewSet import ServiceViewSet
# from ProjectShedulingApp.viewset import (
#     CategoryResourceViewSet, ResourceViewSet, ReservationViewSet,
#     PersonneViewSet, StudentViewSet, TeacherViewSet,
#     DepartmentViewSet, AdministrativeServiceViewSet,
#     MembreAdminViewSet, RequeteViewSet
# )


router = DefaultRouter()
# router.register(r'category-resources', CategoryResourceViewSet)
# router.register(r'resources', ResourceViewSet)
# router.register(r'reservations', ReservationViewSet)

router.register(r'students', StudentViewSet, basename='students')
router.register(r'teachers', TeacherViewSet, basename='teachers')
router.register(r'admin', TeacherViewSet, basename='admin')

router.register(r'classrooms', ResourceViewSet.ClassRoomViewSet, basename='classrooms')

router.register(r'services', ServiceViewSet, basename='services')
# router.register(r'departments', DepartmentViewSet)
# router.register(r'administrative-services', AdministrativeServiceViewSet)
# router.register(r'membre-admins', MembreAdminViewSet)
# router.register(r'requetes', RequeteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login-student/', LoginStudentAPIView.as_view(), name='api-loginstudent'),
    path('login-teacher/', LoginTeacherAPIView.as_view(), name='api-loginteacher'),
    path('login-admin/', LoginTeacherAPIView.as_view(), name='api-loginadmin'),

]