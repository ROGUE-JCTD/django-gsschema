import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-gsschema',
    version='0.1-alpha4',
    author='Syrus Mesdaghi',
    author_email='geoshape.org@gmail.com',
    url='https://github.com/ROGUE-JCTD/django-gsschema',
    download_url='https://github.com/ROGUE-JCTD/django-gsschema',
    description='Service that creates tilesets from layer sources and serves them',
    long_description=open(os.path.join(here, 'README.md')).read(),
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Topic :: Utilities',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=[
        'Django==1.6.10',
    ]
)
