import sys

import gunicorn.app.base

from whitenoise import WhiteNoise


class Application(gunicorn.app.base.BaseApplication):
    def __init__(self, application, port):
        self.application = application
        self.port = port
        super(Application, self).__init__()

    def load_config(self):
        self.cfg.set('bind', '0.0.0.0:{0}'.format(self.port))

    def load(self):
        return self.application


def serve(folder, port):
    application = WhiteNoise(application=None, root=folder)
    app = Application(application, port)
    app.run()


def main():
    serve(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
