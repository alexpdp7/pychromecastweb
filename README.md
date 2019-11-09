# pychromecastweb

THIS PROJECT IS ARCHIVED AS I AM NO LONGER DEVELOPING THIS (NOW I USE
A MIBOX DEVICE WITH KODI SO I NO LONGER REQUIRE THIS).

PLEASE OPEN A TICKET AT:

https://github.com/alexpdp7/alexpdp7

IF YOU REQUIRE SUPPORT

pychromecastweb is a web application that allows you to browse parts of
the local filesystem and cast videos to a Chromecast.

This is in a very rough state. To do something, follow the instructions
below, go to `/admin/`, create a media source pointing to folders with
media files, go back to `/`, browse and cast.

You can also go to `/admin/` to add Chromecasts manually, this is useful
if you are running this on a wired network or the Chromecasts are in a
different subnet.

## DEVELOPMENT

```shell
$ pipenv install --python 3.6 -e .[dev]
$ pipenv run python manage.py migrate
$ pipenv run python manage.py createsuperuser
$ CAST_HOST=<ip of your host> pipenv run gunicorn -b 0.0.0.0:8000 pyccw.wsgi -w 4
```

Chromecasts seem to use Google's public DNS servers, so you need to
specify which host should the Chromecast use to reach the embedded web
server for media files.

## INSTALLATION

This will install it under your user account:

```shell
$ pip3 install --user git+https://github.com/alexpdp7/pychromecastweb.git
$ CAST_HOST=<ip of your host> django-admin migrate --settings pyccw.settings
$ CAST_HOST=<ip of your host> django-admin createsuperuser --settings pyccw.settings
$ gunicorn -b 0.0.0.0:8000 pyccw.wsgi -w 4
```

If `./.local/bin` is not in your path, you might need to prepend it to the
gunicorn and django-admin commands

## CONFIGURATION

Use `PYCCW_LOG_LEVEL=(DEBUG|...)` to configure log levels.

## CONTRIBUTING

PRs are welcome! Please add yourself to the contributors list in the PR.

### Contributors

* Álex Córcoles <alex@corcoles.net> (author)
* Hervé Beraud <herveberaud.pro@gmail.com>
