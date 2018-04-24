#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

setup(name = 'fast_distance',
	version = '4.1',
	description = 'fast computation of distance and similarity between strings',
	author = 'Yves Lepage',
	author_email = 'yves.lepage@waseda.jp',
	ext_modules =	[Extension('_fast_distance',
						sources = ['fast_distance.i', 'fast_distance.c', 'utf8.c'],
						swig_opts=['-modern', '-new_repr'],
						extra_compile_args = ['-std=c99']
					)],
	)

# Inside this directory,
# use the following command to compile:
# sudo -H pip install -e .

# Inside this directory,
# use the following command to test the help:
# ./fast_distance.py -h

# Inside this directory,
# use the following command to test the execution:
# fast_distance.py toto tata
