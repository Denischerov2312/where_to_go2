from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin, SortableTabularInline, SortableAdminBase
from .models import Place, Image


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
    raw_id_fields = ['place']


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
