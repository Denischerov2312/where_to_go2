import json
from pathlib import Path
from django.core.management.base import BaseCommand
from places.models import Place, Image


## TODO Добавить через request загрузку данных

class Command(BaseCommand):
    help = "Загружает файлы json в базу данных"
    
    def handle(self, *args, **options):
        
        for file_path in Path('static/places_json').iterdir():
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    place_obj, create = Place.objects.get_or_create(
                        title=data['title'],
                        description_short=data['description_short'],
                        description_long=data['description_long'],
                        longitude=float(data['coordinates']['lng']),
                        latitude=float(data['coordinates']['lat']),
                    )
                    for number, img in enumerate(data['imgs'], 1):
                        Image.objects.create(
                            place=place_obj,
                            name=f'image{number}',
                            image=img,
                            number=number,
                        )