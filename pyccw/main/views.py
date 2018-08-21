from django import shortcuts
from django.http import HttpResponse
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
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'play':
                services.play(ms, path, file)
            if action == 'pause':
                services.pause()
            if action == 'resume':
                services.resume()
        if 'seek' in request.POST:
            services.seek(int(request.POST['seek']))

    return shortcuts.render(request, 'main/cast.html', {
        'media_source': ms,
        'path': path,
        'file': file,
    })


def subtitle(request, mediasource, path, file):
    ms = shortcuts.get_object_or_404(models.MediaSource, name=mediasource)
    srt = ms.get_sub_path(path) / file.replace('.vtt', '.srt')
    vtt = services.convert_to_vtt(srt)
    response = HttpResponse(content_type='text/vtt')
    response.write(vtt)
    return response
