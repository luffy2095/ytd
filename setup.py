#!/usr/bin/env python

import os

from setuptools import setup, find_packages

if os.environ.get('USER', '') == 'vagrant':
  del os.link

setup(
  name = 'YtbDwn',
  packages = ['YtbDwn'], # this must be the same as the name above
  version = '0.2',
  description = 'Youtube Downloader with TUI',
  author = 'Praneet Sherki',
  author_email = 'sherkipraneet@gmail.com',
  url = 'https://github.com/praneet95/YtbDwn', # use the URL to the github repo
  download_url = 'https://github.com/praneet95/YtbDwn/tarball/0.1', # I'll explain this in a second
  keywords = ['Youtube ', 'Downloader', 'TUI'], # arbitrary 
  install_requires=[
    'pafy == 0.4.3',
    'pyperclip == 1.5.26',
    'selenium == 2.52.0',
    'urwid == 1.3.1',
    'beautifulsoup4 == 4.4.1'
  	],
  entry_points={
    'console_scripts': [
        'ytbdwn = YtbDwn.ytbdwn'
    ],
    }
)



