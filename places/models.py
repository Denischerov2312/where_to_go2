from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название места', max_length=150)
    short_description = models.TextField('Короткое описание')
    long_description = HTMLField('Длинное описание')
    longitude = models.FloatField('Долгота')
    latitude = models.FloatField('Широта')

    def __str__(self):
        return self.title


class Image(models.Model):
    number = models.IntegerField('Номер', default=0)
    name = models.CharField('Имя')
    image = models.ImageField('Картинка')
    place = models.ForeignKey(Place,
                              on_delete=models.CASCADE,
                              related_name='images',
                              blank=True,
                              null=True,
                              verbose_name='Место, к которому привязана картинка'
                              )

    def __str__(self):
        return f"{self.number} {self.name}"

    class Meta:
        ordering = ['number']
