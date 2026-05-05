import json
import requests
from pathlib import Path
from django.core.management.base import BaseCommand
from places.models import Place, Image
from os.path import join
from os import makedirs



class Command(BaseCommand):
    help = "Загружает файлы json и данные из них в базу данных"
    saved_path = 'static/places'

    def download_github_json(self, owner='devmanorg', repo='where-to-go-places', download_dirs='places'):
        github_url = join(f'https://api.github.com/repos/{owner}/{repo}/contents/',  download_dirs)
        response = requests.get(github_url)
        response.raise_for_status()
        files = response.json()
        for file_info in files:
            if file_info['name'].endswith('.json'):
                file_response = requests.get(file_info['download_url'])
                file_response.raise_for_status()
                file_data = file_response.json()
                makedirs(self.saved_path, exist_ok=True)
                with open(join(self.saved_path, file_info['name']), 'w', encoding='utf-8') as file:
                    json.dump(file_data, file, ensure_ascii=False)

    def handle(self, *args, **options):
        self.download_github_json()

        for file_path in Path('static/places').iterdir():
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as file:
                    place_details = json.load(file)
                    place_obj, create = Place.objects.get_or_create(
                        title=place_details['title'],
                        short_description=place_details['description_short'],
                        long_description=place_details['description_long'],
                        longitude=float(place_details['coordinates']['lng']),
                        latitude=float(place_details['coordinates']['lat']),
                    )
                    for number, img in enumerate(place_details['imgs'], 1):
                        Image.objects.create(
                            place=place_obj,
                            image=img,
                            number=number,
                        )