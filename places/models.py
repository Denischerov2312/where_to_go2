from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=150)
    description_short = models.TextField()
    description_long = models.TextField()
    coordinates = models.JSONField(default=dict)

    def __str__(self):
        return self.title


class Image(models.Model):
    number = models.IntegerField()
    name = models.CharField()
    image = models.ImageField()

    def __str__(self):
        return f"{self.number} {self.name}"
