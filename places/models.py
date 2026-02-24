from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=150)
    description_short = models.TextField()
    description_long = HTMLField()
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.title


class Image(models.Model):
    number = models.IntegerField(default=0)
    name = models.CharField()
    image = models.ImageField()
    place = models.ForeignKey(Place,
                              on_delete=models.CASCADE,
                              related_name='images',
                              blank=True,
                              null=True,
                              )

    def __str__(self):
        return f"{self.number} {self.name}"

    class Meta:
        ordering = ['number']
