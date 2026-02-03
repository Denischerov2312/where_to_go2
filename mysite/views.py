from django.http import HttpResponse
from django.template import loader
from places.models import Place
from places.models import Image


def get_geojson():
    geo_json = {
      "type": "FeatureCollection",
      "features": []
    }
    Places = Place.objects.all()
    Images = Image.objects.all()
    for i in range(len(Places)):
        coordinates = Places[i].coordinates
        feature = {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [float(coordinates['lng']), float(coordinates['lat'])]
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


def show_title(request, place_id):
    return HttpResponse(Place.objects.get(id=place_id).title)


def show(request):
    template = loader.get_template('index.html')
    context = {
                'geo_json': get_geojson(),
                'sidebar_js_filepath': 'leaflet-sidebar.js',
                'favicon_filepath': 'favicon.png',
                'sidebar_css_filepath': 'leaflet-sidebar.css',
                'svg_filepath': 'hand-pointer-regular.svg',
               }
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)
