import json
from os.path import join, basename
from os import makedirs
from pathlib import Path

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from places.models import Place, Image


class Command(BaseCommand):
    help = "Загружает файлы json и данные из них в базу данных"
    saved_path = 'static/places'

    def download_github_json(self, owner='devmanorg', repo='where-to-go-places', download_dirs='places'):
        github_url = join(f'https://api.github.com/repos/{owner}/{repo}/contents/',  download_dirs)
        response = requests.get(github_url)
        response.raise_for_status()
        files = response.json()
        self.stdout.write(f"Загрузка данных json из {github_url}")
        for file_info in files:
            if file_info['name'].endswith('.json'):
                file_response = requests.get(file_info['download_url'])
                file_response.raise_for_status()
                file_data = file_response.json()
                makedirs(self.saved_path, exist_ok=True)
                with open(join(self.saved_path, file_info['name']), 'w', encoding='utf-8') as file:
                    json.dump(file_data, file, ensure_ascii=False)
                self.stdout.write(self.style.SUCCESS(f"Успешно загружено: {file_info['name']}"))

    def download_img(self, img_url):
        response = requests.get(img_url)
        response.raise_for_status()
        filename = basename(img_url)
        img_content = ContentFile(response.content, name=filename)
        return img_content

    def handle(self, *args, **options):
        self.download_github_json()
        self.stdout.write("Импорт данных в базу")
        for file_path in Path(self.saved_path).iterdir():
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as file:
                    place_details = json.load(file)
                    place_obj, place_created = Place.objects.get_or_create(
                        title=place_details['title'],
                        short_description=place_details['description_short'],
                        long_description=place_details['description_long'],
                        longitude=float(place_details['coordinates']['lng']),
                        latitude=float(place_details['coordinates']['lat']),
                    )
                    if place_created:
                        self.stdout.write(self.style.SUCCESS(f"Добавлено место: {place_obj.title}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Место: {place_obj.title} уже есть в базе"))
                    for number, img_url in enumerate(place_details['imgs'], 1):
                        image_obj, created = Image.objects.get_or_create(
                            place=place_obj,
                            number=number
                        )
                        if created:
                            image_obj.image = self.download_img(img_url)
                            image_obj.save()
                            self.stdout.write(f"Загружена картинка: {basename(image_obj.image.name)}")
