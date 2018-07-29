from django import shortcuts
from django.views import generic

from pyccw.main import models


class MediaSourceListView(generic.ListView):
    model = models.MediaSource


def mediasource_path(request, mediasource, path=''):
    ms = shortcuts.get_object_or_404(models.MediaSource, name=mediasource)
    return shortcuts.render(request, 'main/mediasource_path.html', {
        'media_source': ms,
        'path': path,
        'folders': ms.get_folders(path),
        'media_files': ms.get_media_files(path),
    })


def cast(request, mediasource, path, file):
    return 'foo'
