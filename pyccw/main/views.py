from django.views import generic

from pyccw.main import models


class MediaSourceListView(generic.ListView):
    model = models.MediaSource
