from django.urls import include,path
from rest_framework.routers import DefaultRouter

from ProjectShedulingApp.viewset import ( 
  
    StudentViewSet,
    TeacherViewSet,
    OrdinateurViewSet,
    VideoProjecteurViewSet,
    SalleDeClasseViewSet,
    MembreAdminViewSet,
      AdministrativeServiceViewSet,
    ReservationViewSet,
    RequeteViewSet,
    DepartmentViewSet,
    LoginTeacherAPIView,
   LoginStudentAPIView,
    LoginMembreAdminAPIView,
    ContextViewSet
)
# from ProjectShedulingApp.viewset.ContextViewset import ContextViewSet



router = DefaultRouter()

router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'computers', OrdinateurViewSet)
router.register(r'projectors', VideoProjecteurViewSet)
router.register(r'classrooms', SalleDeClasseViewSet)
router.register(r'services-administratifs', AdministrativeServiceViewSet)
router.register(r'membres-administratifs', MembreAdminViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'requests', RequeteViewSet)
router.register(r'departments', DepartmentViewSet)  # Ajout de l'URL pour le département
router.register(r'context', ContextViewSet,basename='context')  # Ajout de l'URL pour le contexte

urlpatterns = [
    path('', include(router.urls)),
      path('login-teacher/', LoginTeacherAPIView.as_view(), name='login-teacher'),
    path('login-student/', LoginStudentAPIView.as_view(), name='login-student'),
    path('login-membre-admin/', LoginMembreAdminAPIView.as_view(), name='login-membre-admin'),
]