# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

setup(
    name="Pr1",
    version="1.0",
    description="Practica 3",
    author="Álvaro Penalva Alberca y Pablo Jiménez Cruz",
    author_email="",
    url="",
    license="tipo de licencia",
    scripts=["main.py"],
    console=["main.py"],
    options={"py2exe": {"bundle_files": 1}},
    zipfile=None,
)