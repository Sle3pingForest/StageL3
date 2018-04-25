#!/usr/bin/python
# coding: utf-8

import sys
import time
import itertools

from _fast_distance import init_memo_fast_distance, memo_fast_distance, memo_fast_similitude, fast_distance
from _nlg import solvenlg, verifnlg

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>'
__date__, __version__ = '10/10/2017', '1.0'
__description__ = '''
	Module for enumeration strategies.
'''
__verbose__ = False

#################################################################################

def direct_iteration_strategy(self, string=None, strategy='naive'):
	"""
	If no Bs, then just iterate over the keys in the order of the dictionary.
	Else, apply the stategy selected to enumerate the source sentences in the bicorpus.
	There are 3 possible strategies implemented:
		naive: no sort is performed.
				The sentences are just enumerated in the order
				in which they appear in the bicorpus.
		by distance: the sentences are enumerated by increasing
				distance to the sentence to be translated.
				The LCS distance is used.
		by similitude: the sentences are enumerated by decreasing
				similarity with the sentence to be translated.
				Similitude is the length of the longest common
				subsequence (LCS).
	"""
	Bs = string
	if __verbose__: print >> sys.stderr, 'Bs = "%s", strategy = %s' % (Bs, strategy)
	if Bs == None or strategy == 'naive':
		result = self.keys()
		print 'je ne passe pas dans naive '
	else:
		init_memo_fast_distance(Bs)
		if strategy == 'by distance':
			result = sorted(self.keys(), key=lambda Xs: memo_fast_distance(Xs))
		elif strategy == 'by similitude':
			result = sorted(self.keys(), key=lambda Xs: memo_fast_similitude(Xs), reverse=True)
	for As in result:
		A = As.rstrip('\n').split('\t')
		if memo_fast_distance(As) == 0:
			yield As, self[As]
			exit(0)
		
		yield As, self[As]
	

#################################################################################

def indirect_iteration_strategy(self, string=None, strategy='naive'):
	"""
	If no Bs, then just output all triples of sentences in the order
		of the bicorpus.
	Else, apply the stategy selected to enumerate the source sentences in the bicorpus.
	There are 2 possible strategies implemented:
		naive: no sort is performed.
				Just output all triples of sentences in the order
				of the bicorpus.
		by distance: the As, Bs and Cs are enumerated by increasing
				distance to the sentence to be translated.
	"""
	Ds = string
	if __verbose__: print >> sys.stderr, 'Ds = "%s", strategy = %s' % (Ds, strategy)
	if Ds == None or strategy == 'naive':
		for triple in itertools.product(self, repeat=3):
			yield triple
	else:
		init_memo_fast_distance(Ds)
		if strategy == 'by distance':
			init_memo_fast_distance(Ds)
			closest_As = sorted(self.keys(), key=lambda Xs: memo_fast_distance(Xs))[:100]
			for triple in sorted(itertools.product(closest_As, repeat=3)):
				As, Bs, Cs = triple
				if As != Bs and As != Cs and Bs != Cs:
					if __verbose__: print >> sys.stderr, '# {} : {} :: {} : {}'.format(As, Bs, Cs, Ds)
					yield triple
		elif strategy == 'closest':
			first_N = 3
			init_memo_fast_distance(Ds)
			for Bs in sorted(self.keys(), key=lambda Xs: memo_fast_distance(Xs))[:first_N]:
				init_memo_fast_distance(Bs)
				for As in sorted(self.keys(), key=lambda Xs: len(Bs) - memo_fast_similitude(Xs))[:first_N]:
					if __verbose__: print >> sys.stderr, '# {} : {} :: {} : x'.format(Bs, As, Ds)
					CCs = solvenlg(Bs, As, Ds)
					if CCs != None:
						if __verbose__: print >> sys.stderr, '# {} : {} :: {} : {}'.format(Bs, As, Ds, CCs)
						init_memo_fast_distance(CCs)
						for Cs in sorted(self.keys(), key=lambda Xs: memo_fast_distance(Xs))[:first_N]:
							if __verbose__: print >> sys.stderr, '# {} : {} :: {} : {}'.format(Bs, As, Ds, Cs)
							yield (As, Bs, Cs)

#################################################################################

iteration_strategy = {
	'direct':	direct_iteration_strategy,
	'indirect': indirect_iteration_strategy
}

#################################################################################
