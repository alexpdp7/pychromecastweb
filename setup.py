from setuptools import setup, find_packages

setup(name='pychromecastweb',
      packages=find_packages(),
      install_requires=['pychromecast','Django'],
      extras_require={
        'dev': ['ipython', 'ipdb',],
      },
      python_requires='>=3',
)
      