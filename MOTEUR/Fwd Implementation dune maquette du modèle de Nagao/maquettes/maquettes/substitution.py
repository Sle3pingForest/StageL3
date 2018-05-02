#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>'
__date__, __version__ = '10/10/2017', '1.0'
__description__ = '''
	Module to extract substitutions.
'''
__verbose__ = True

################################################################################

def single_substitution(As, Bs):
	"""
	Extract a single substitution between two strings.
	>>> single_substitution('this is an example', 'that is an example')
	('is', 'at')
	>>> single_substitution('Well, this is an example', 'Well, that is an example')
	('is', 'at')
	>>> single_substitution('I love apples.', 'They love apples.')
	('I', 'They')
	"""
	from os.path import commonprefix

	def commonsuffix(list):
		return commonprefix([s[::-1] for s in list])[::-1]
	
	prefix, suffix = commonprefix([As, Bs]), commonsuffix([As, Bs])
	if __verbose__ and As == 'They love pears.': print >> sys.stderr, 'prefix/suffix({}, {}) = {}, {}'.format(As, Bs, prefix, suffix)
	return As[len(prefix):-len(suffix)], Bs[len(prefix):-len(suffix)]

################################################################################

def tree_substitution(As, Bs):
	"""
	Extract a tree of substitutions which are possible between two strings As and Bs.
	For that recursively compute the longest common substrings (not subsequences).
	In fact, same as CharCut.
	NOT IMPLEMENTED.
	"""
	return None
