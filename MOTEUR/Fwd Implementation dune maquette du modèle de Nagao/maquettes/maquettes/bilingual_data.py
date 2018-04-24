#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

from enumeration import iteration_strategy
from _fast_distance import init_memo_fast_distance, memo_fast_distance, memo_fast_similitude

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>'
__date__, __version__ = '10/10/2017', '1.0'
__description__ = '''
	Module for bilingual data.
'''
__verbose__ = False

################################################################################

class Bicorpus(dict):

	type_name = 'Bicorpus'

	def __init__(self, bidata={}):
		self.type = type
		for key in bidata:
			self[key] = bidata[key]
		if __verbose__: print >> sys.stderr, '\n# {}:\n{}'.format(type(self).type_name, self)

	@classmethod
	def fromFile(cls, file=sys.stdin, source=0, target=1):
		"""
		The file is made out of lines containing a sentence in different languages separated by tabulations.
		The source and target arguments are the column numbers for the source and target languages.
		"""
		bidata = {}
		for line in file:
			print line
			A = line.rstrip('\n').split('\t')
			bidata[A[source]] = A[target]
		return cls(bidata=bidata)

	def __add__(self, other):
		for As in other:
			if As not in self:
				self[As] = other[As]
		return self

	def iter(self, string=None, strategy='naive', method='direct'):
		return iteration_strategy[method](self, string, strategy)

	def __repr__(self):
		return '\n'.join( '{}\t{}'.format(As, self[As]) for As in self )

################################################################################

class Bidictionary(Bicorpus):

	type_name = 'Bidictionary'

################################################################################

