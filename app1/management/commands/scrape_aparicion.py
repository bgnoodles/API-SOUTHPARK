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
                aparicion = soup.find_all('p')
                for p in aparicion:
                    texto_completo = p.get_text(strip=True)
                    if "episodio" in texto_completo:
                        episodio = p.find('a')
                        if episodio:
                            titulo = episodio.get_text(strip=True)
                            personaje.primera_aparicion = titulo
                            personaje.save()
                            self.stdout.write(self.style.SUCCESS(f"Actualizada la primera aparición de {personaje.nombre} a '{titulo}'"))
                        else:
                            self.stdout.write(self.style.WARNING(f"No se encontró el título del episodio para {personaje.nombre}"))
                        break
            else:
                self.stdout.write(self.style.WARNING(f"No se encontró la información de primera aparición para {personaje.nombre}"))