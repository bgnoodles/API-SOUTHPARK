from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from app1.models import Personaje
from datetime import datetime
import locale, re

class Command(BaseCommand):
    help = 'Actualiza la información de personajes de South Park'

    def handle(self, *args, **kwargs):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        personajes = Personaje.objects.all()

        for personaje in personajes:
            personaje_url = f'https://southpark.fandom.com/es/wiki/{personaje.nombre.replace(" ", "_")}'
            response = requests.get(personaje_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                fecha_nacimiento = soup.find_all('div', class_='pi-data-value pi-font')

                if fecha_nacimiento:
                    if len(fecha_nacimiento) > 2:
                        fecha_nacimiento_texto = fecha_nacimiento[2].get_text(strip=True)
                        
                        # Imprimir el texto extraído para depuración
                        self.stdout.write(self.style.NOTICE(f"Texto extraído: '{fecha_nacimiento_texto}'"))

                        # Manejo de edades con rango
                        if '-' in fecha_nacimiento_texto:
                            # Filtrar solo los números antes de convertir
                            edades = [int(edad) for edad in fecha_nacimiento_texto.split('-') if edad.strip().isdigit()]
                            if edades:
                                personaje.edad = max(edades)
                                personaje.save()
                                self.stdout.write(self.style.SUCCESS(f"Actualizada la edad de {personaje.nombre} a {personaje.edad} años"))
                            else:
                                self.stdout.write(self.style.WARNING(f"No se encontraron edades válidas en el rango para {personaje.nombre}"))

                        # Manejo de edad exacta
                        elif fecha_nacimiento_texto.isdigit():
                            personaje.edad = int(fecha_nacimiento_texto)
                            personaje.save()
                            self.stdout.write(self.style.SUCCESS(f"Actualizada la edad de {personaje.nombre} a {personaje.edad} años"))
                        
                        # Manejo de casos no numéricos, buscando números
                        else:
                            numeros_en_texto = re.findall(r'\d+', fecha_nacimiento_texto)
                            if numeros_en_texto:
                                personaje.edad = int(numeros_en_texto[0])
                                personaje.save()
                                self.stdout.write(self.style.SUCCESS(f"Actualizada la edad de {personaje.nombre} a {personaje.edad} años"))
                            else:
                                self.stdout.write(self.style.WARNING(f"No se pudo determinar la edad para {personaje.nombre}"))

                        # Intentar extraer la fecha de nacimiento
                        try:
                            fecha_nacimiento_date = datetime.strptime(fecha_nacimiento_texto, '%d de %B de %Y')
                            edad = (datetime.now() - fecha_nacimiento_date).days // 365
                            personaje.edad = edad
                            personaje.save()
                            self.stdout.write(self.style.SUCCESS(f"Actualizada la edad de {personaje.nombre} a {edad} años"))
                        except ValueError as e:
                            self.stdout.write(self.style.WARNING(f"Error al procesar la fecha para {personaje.nombre}: {e}. Texto de fecha: '{fecha_nacimiento_texto}'"))
                    else:
                        self.stdout.write(self.style.WARNING(f"No hay suficientes datos para {personaje.nombre}."))
                else:
                    self.stdout.write(self.style.WARNING(f"No se encontró la fecha de nacimiento para {personaje.nombre}"))
