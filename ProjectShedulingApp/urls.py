from django.urls import include,path
from rest_framework.routers import DefaultRouter

from ProjectShedulingApp.viewset import ( 
    StudentViewSet,
    TeacherViewSet,
    OrdinateurViewSet,
    VideoProjecteurViewSet,
    SalleDeClasseViewSet,
    MembreAdminViewSet,
      AdministrativeServiceViewSet

)



router = DefaultRouter()

router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'ordinateurs', OrdinateurViewSet)
router.register(r'video-projecteurs', VideoProjecteurViewSet)
router.register(r'salles-de-classe', SalleDeClasseViewSet)
router.register(r'services-administratifs', AdministrativeServiceViewSet)
router.register(r'membres-administratifs', MembreAdminViewSet)

# router.register(r'requetes', RequeteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]