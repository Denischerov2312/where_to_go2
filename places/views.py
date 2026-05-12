from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.urls import reverse
from places.models import Place


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
        'geo_json': {
            'type': 'FeatureCollection',
            'features': features
        }
    }
    template = loader.get_template('index.html')
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def show_place(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related('images'), id=place_id)
    images_urls = [image.image.url for image in place.images.all()]
    payload = {
        'title': place.title,
        'imgs': images_urls,
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude,
        }
    }
    return JsonResponse(payload, json_dumps_params={'ensure_ascii': False})
