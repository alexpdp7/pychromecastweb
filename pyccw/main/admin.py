from django.contrib import admin

from pyccw.main import models


admin.site.register(models.MediaSource)
admin.site.register(models.Chromecast)