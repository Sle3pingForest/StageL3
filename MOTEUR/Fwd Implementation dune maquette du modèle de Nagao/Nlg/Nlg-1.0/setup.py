#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, Extension

setup(name = 'Nlg',
	version = '1.0',
	description = 'Analogical clustering',
	author = 'Yves Lepage & Fam Rashel',
	author_email = 'yves.lepage@waseda.jp & fam.rashel@fuji.waseda.jp',
	ext_modules =	[Extension('_nlg',
						sources = ['nlg/Analogy/C/nlg.i', 'nlg/Analogy/C/nlg.c', 'nlg/Analogy/C/utf8.c'],
						swig_opts=['-modern', '-new_repr'],
						extra_compile_args = ['-std=c99']),
					 Extension('_nlgclu',
						sources = ['nlg/Cluster/Words2Clusters/nlgclu_in_C/nlgclu.i', 'nlg/Cluster/Words2Clusters/nlgclu_in_C/nlgclu.c'],
						swig_opts=['-modern', '-new_repr']
					)],
	)

# Use the following command to compile (-e is optional):
# sudo -H pip install [-e] .

# Use the following command to test the help:
# python2 Words2Clusters.py -h

# Use the following commands to test the execution:
# printf "toto\ntata\npopo\npapa\n" | python2 Words2Clusters.py -V
