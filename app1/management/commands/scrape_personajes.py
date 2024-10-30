from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from app1.models import Personaje

class Command(BaseCommand):
    help = 'Scrapea personajes de South Park'

    def handle(self, *args, **kwargs):
        url = 'https://southpark.fandom.com/es/wiki/Categoría:Personajes'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        lista_alfabeto = soup.find_all('div', class_='category-page__members-wrapper')

        for letra in lista_alfabeto:
            lista_personajes = letra.find('ul', class_='category-page__members-for-char')

            if lista_personajes:
                personajes_li = lista_personajes.find_all('li')

                for li in personajes_li:
                    enlace = li.find('a')
                    if enlace and 'title' in enlace.attrs:
                        nombre = enlace['title']
                        if not nombre.startswith("Categoría:") and not nombre.startswith("Familias"):
                            nuevo_personaje = Personaje(nombre=nombre, edad=None, imagen_url='', primera_aparicion='', ocupacion='')
                            nuevo_personaje.save()
                            self.stdout.write(self.style.SUCCESS(f"Personaje guardado: {nombre}"))
                        else:
                            self.stdout.write(self.style.WARNING(f"Filtrado: {nombre} (categoria no guardada)"))
