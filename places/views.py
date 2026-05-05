from django.http import HttpResponse
from django.template import loader
from places.models import Place
from places.models import Image
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse


def start_page(request):
    places = Place.objects.all()
    features = [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.longitude, place.latitude]
            },
            'properties': {
                'title': place.title,
                'placeId': place.id,
                'detailsUrl': reverse('parse_place_details',
                                      kwargs={'place_id': place.id})
            }
        } for place in places
    ]
    context = {
        'places': {
            'type': 'FeatureCollection',
            'features': features
        }
    }
    return render(request, 'index.html', context)


def show_place(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related('images'), id=place_id)
    place = get_object_or_404(Place.objects, id=place_id)
    images_urls = [image.image.url for image in place.images.all()]

    payload = {
        'title': place.title,
        'imgs': images_urls,
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude,
        }
    }
    return JsonResponse(payload, json_dumps_params={'ensure_ascii': False})


def get_geojson():
    geo_json = {
      "type": "FeatureCollection",
      "features": []
    }
    Places = Place.objects.all()
    for i in range(len(Places)):
        feature = {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [Places[i].longitude, Places[i].latitude]
          },
          "properties": {
            "title": Places[i].title,
            "placeId": "moscow_legends",
            "detailsUrl": "static/places/moscow_legends.json"
          }
        }
        geo_json["features"].append(feature)
    print(len(geo_json['features']))
    return geo_json


def show(request):
    template = loader.get_template('index.html')
    context = {
                'geo_json': get_geojson(),
               }
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)
