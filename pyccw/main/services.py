import socket
import subprocess
import time

from django.conf import settings

import pychromecast


EXCLUDED_MODELS = ['Google Home Mini']


def play(mediasource, path, file):
    url = spawn_server(mediasource.get_sub_path(path), file)
    content_type = 'video/{0}'.format(file.split('.')[-1])
    get_chromecast().play_media(url, content_type)


def pause():
    get_chromecast().media_controller.pause()


def resume():
    get_chromecast().media_controller.play()


def seek(delta):
    chromecast = get_chromecast()
    chromecast.media_controller.seek(chromecast.media_controller.status.current_time + delta)


def get_chromecasts():
    chromecasts = pychromecast.get_chromecasts()
    return [cc for cc in chromecasts if cc.model_name not in EXCLUDED_MODELS]


def get_chromecast():
    chromecasts = get_chromecasts()
    assert len(chromecasts) == 1
    chromecast = chromecasts[0]
    chromecast.media_controller.block_until_active()
    return chromecast


def get_hostname():
    # return socket.gethostname()  # Chromecasts use Google's DNS, so this doesn't work
    return settings.CAST_HOST


def spawn_server(path, file):
    s = subprocess.Popen(['pyccw_serve', path, '0'], stdout=subprocess.PIPE)
    while True:
        try:
            out = subprocess.check_output(['lsof', '-P', '-a', '-p', str(s.pid), '-i', 'TCP', '-sTCP:LISTEN'])
            break
        except subprocess.CalledProcessError:
            time.sleep(1)
    port = int(str(out).split()[-2].split(':')[1])
    return 'http://{0}:{1}/{2}'.format(get_hostname(), port, file)
