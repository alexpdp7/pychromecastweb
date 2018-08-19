from django import shortcuts
from django.views import generic

from pyccw.main import models
from pyccw.main import services


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
    ms = shortcuts.get_object_or_404(models.MediaSource, name=mediasource)
    if request.POST:
        action = request.POST['action']
        if action == 'play':
            services.play(ms, path, file)
        if action == 'pause':
            services.pause()
        if action == 'resume':
            services.resume()
        if action == 'backward_10':
            services.seek(-10)
        if action == 'forward_10':
            services.seek(10)

    return shortcuts.render(request, 'main/cast.html', {
        'media_source': ms,
        'path': path,
        'file': file,
    })
