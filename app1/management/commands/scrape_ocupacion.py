from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from app1.models import Personaje

class Command(BaseCommand):
    help = 'Actualiza la información de personajes de South Park'

    def handle(self, *args, **kwargs):
        personajes = Personaje.objects.all()

        for personaje in personajes:
            personaje_url = f'https://southpark.fandom.com/es/wiki/{personaje.nombre.replace(" ", "_")}'
            response = requests.get(personaje_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                ocupacion = soup.find('div', attrs={'data-source': 'Trabajo'})
                
                # Verificar que 'ocupacion' no sea None
                if ocupacion:
                    trabajo = ocupacion.find('div', class_="pi-data-value pi-font")
                    if trabajo:
                        trabajo_texto = trabajo.get_text(strip=True)
                        personaje.ocupacion = trabajo_texto
                        personaje.save()
                        self.stdout.write(self.style.SUCCESS(f"Actualizada la ocupación de {personaje.nombre} a '{trabajo_texto}'"))
                    else:
                        self.stdout.write(self.style.WARNING(f"No se encontró la información de trabajo para {personaje.nombre}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No se encontró la sección de ocupación para {personaje.nombre}"))
            else:
                self.stdout.write(self.style.ERROR(f"Error al acceder a la página de {personaje.nombre}: {response.status_code}"))
