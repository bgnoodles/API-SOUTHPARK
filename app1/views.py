from django.shortcuts import render
from rest_framework import viewsets
from .models import Personaje
from .serializers import PersonajeSerializer

# Create your views here.
class PersonajeViewset(viewsets.ModelViewSet):
    queryset = Personaje.objects.all()
    serializer_class = PersonajeSerializer
