from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonajeViewset

router = DefaultRouter()
router.register(r'personajes', PersonajeViewset)

urlpatterns = [
    path('',include(router.urls))
]