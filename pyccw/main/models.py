import pathlib

from django.db import models


class MediaSource(models.Model):
    name = models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def _get_root_path(self):
        return pathlib.Path(self.path)

    def get_sub_path(self, sub_path):
        return self._get_root_path() / sub_path

    def get_folders(self, sub_path):
        return [{'mediasource': self, 'name': p.name, 'path': pathlib.Path(sub_path) / pathlib.Path(p.name) } for p in self.get_sub_path(sub_path).iterdir() if p.is_dir()]

    def get_media_files(self, sub_path):
        return [{'name': p.name, 'path': sub_path, 'mediasource': self} for p in self.get_sub_path(sub_path).iterdir() if p.is_file()]
