from django.contrib import admin

from images.models import Image, Post


class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ('uploaded_at', )
    list_display = ('__str__', 'uploaded_at')


admin.site.register(Image, ImageAdmin)
admin.site.register(Post)

