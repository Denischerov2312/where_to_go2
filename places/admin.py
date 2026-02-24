from django.contrib import admin
from .models import Place, Image
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableTabularInline
from adminsortable2.admin import SortableAdminBase


class ImageInline(SortableTabularInline):
    model = Image
    readonly_fields = ['image_preview']
    extra = 1

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain;" />',
                obj.image.url
            )
        return '-'


@admin.register(Image)
class ImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    ordering = ['number']


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
