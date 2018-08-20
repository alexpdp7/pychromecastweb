from setuptools import setup, find_packages

setup(name='pychromecastweb',
      packages=find_packages(),
      install_requires=['pychromecast','Django', 'whitenoise==4.0b5', 'gunicorn', 'webvtt-py', 'django-cors-headers'],
      extras_require={
        'dev': ['ipython', 'ipdb',],
      },
      python_requires='>=3',
      entry_points = {
          'console_scripts': ['pyccw_serve=pyccw.serve:main'],
      },
      include_package_data=True,
)
