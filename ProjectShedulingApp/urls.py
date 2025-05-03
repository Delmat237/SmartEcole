from django.urls import include,path
from rest_framework.routers import DefaultRouter

from ProjectShedulingApp.viewset import StudentViewSet,TeacherViewSet
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

router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
# router.register(r'departments', DepartmentViewSet)
# router.register(r'administrative-services', AdministrativeServiceViewSet)
# router.register(r'membre-admins', MembreAdminViewSet)
# router.register(r'requetes', RequeteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]