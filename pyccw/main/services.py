import logging
import subprocess
import sys
import tempfile
import time

from django.conf import settings

import pychromecast

import webvtt

from pyccw.main import models


LOG = logging.getLogger(__name__)
EXCLUDED_MODELS = ['Google Home Mini']


def play(mediasource, path, file):
    url = spawn_server(mediasource.get_sub_path(path), file)
    extension = file.split('.')[-1]
    content_type = 'video/{0}'.format(extension)
    subtitles = 'http://{0}:8000/subtitle/{1}/{2}/{3}'.format(get_hostname(), mediasource.name, path, file.replace(extension, 'srt'))
    media_controller = get_chromecast().media_controller
    media_controller.play_media(url, content_type, subtitles=subtitles)
    media_controller.block_until_active()
    media_controller.enable_subtitle(1)


def pause():
    media_controller = get_chromecast().media_controller
    media_controller.block_until_active()
    media_controller.pause()


def resume():
    media_controller = get_chromecast().media_controller
    media_controller.block_until_active()
    media_controller.play()


def seek(delta):
    media_controller = get_chromecast().media_controller
    media_controller.block_until_active()
    media_controller.seek(chromecast.media_controller.status.current_time + delta)


def get_chromecasts():
    LOG.debug('looking for chromecasts')
    chromecasts = pychromecast.get_chromecasts()
    LOG.debug('found %s', chromecasts)
    chromecasts += [cc.get_chromecast() for cc in models.Chromecast.objects.all()]
    return [cc for cc in chromecasts if cc.model_name not in EXCLUDED_MODELS]


chromecast = None

def get_chromecast():
    global chromecast

    if chromecast:
        return chromecast
    chromecasts = get_chromecasts()
    assert len(chromecasts) == 1, 'not exactly one chromecast found: {0}'.format(chromecasts)
    chromecast = chromecasts[0]
    LOG.debug('using chromecast %s', chromecast)
    return chromecast


def get_hostname():
    # return socket.gethostname()  # Chromecasts use Google's DNS, so this doesn't work
    return settings.CAST_HOST


def spawn_server(path, file):
    s = subprocess.Popen([sys.executable, '-m', 'pyccw.serve', str(path), '0'], stdout=subprocess.PIPE)
    while True:
        try:
            out = subprocess.check_output(['lsof', '-P', '-a', '-p', str(s.pid), '-i', 'TCP', '-sTCP:LISTEN'])
            break
        except subprocess.CalledProcessError:
            time.sleep(1)
    port = int(str(out).split()[-2].split(':')[1])
    return 'http://{0}:{1}/{2}'.format(get_hostname(), port, file)


def convert_to_vtt(srt_path):
    srt_content = None
    for encoding in ['utf-8', 'iso-8859-1',]:
        try:
            with open(str(srt_path), encoding=encoding) as f:
                srt_content = f.read().strip()
                break
        except UnicodeDecodeError:
            pass
    assert srt_content, 'no detectable encoding'
    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', encoding='utf-8', delete=False) as tmp_srt:
        tmp_srt.write(srt_content)
    webvtt.from_srt(tmp_srt.name).save()
    with open(tmp_srt.name.replace('.srt', '.vtt')) as vtt:
        return vtt.read()
