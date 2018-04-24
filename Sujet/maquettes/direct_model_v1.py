#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

from bilingual_data import Bicorpus, Bidictionary
from substitution import single_substitution

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>'
__date__, __version__ = '10/10/2017', '1.0'
__description__ = '''
	Translates the sentences given on the standard input
	using Nagao's direct model of translation by analogy.
	For that, uses the bicorpus and the bilingual dictionary
	passed as positional arguments.
'''
__verbose__ = False

################################################################################

def read_argv():

	import argparse
	this_version = 'v%s (c) %s %s' % (__version__, __date__.split('/')[2], __author__)
	this_description = __description__
	this_usage = '''
		%(prog)s  CORPUS  DICTIONARY
	'''

	parser = argparse.ArgumentParser(version=this_version, description=this_description, usage=this_usage)
	corpus_and_dictionary_help = 'the bi- or multi-lingual %(dest)s (see options -s and -t)'
	parser.add_argument('corpus', metavar='CORPUS',
					action='store', default=None,
					help=corpus_and_dictionary_help)
	parser.add_argument('dictionary', metavar='DICTIONARY',
					action='store', default=False,
					help=corpus_and_dictionary_help)
	source_and_target_help = 'column of the %(dest)s language in the corpus and the dictionary (starts with 0, default: %(default)d)'
	parser.add_argument('-s', '--source',
					action='store', type=int, default=0,
					help=source_and_target_help)
	parser.add_argument('-t', '--target',
					action='store', type=int, default=1,
					help=source_and_target_help)
	parser.add_argument('-V', '--verbose',
					action='store_true',
					help='verbose mode')

	return parser.parse_args()

################################################################################

def translate(bicorpus, bidictionary, file=sys.stdin):
	"""
	input: Bs in the source language
	output: list of Bt in the target language, candidate translations
	data (passed as argument):
		bicorpus = list of pairs (As, At) where At is the translation of As.
		bidictionary = bilingual dictionary of (a_s, a_t) where a_s is a word, and a_t its translation.
	"""
#	bidictionary = bicorpus
	for Bs in file:
		Bs = Bs.rstrip('\n')
		if __verbose__: print >> sys.stderr, '\n# Translating sentence: {}'.format(Bs)
		for As in bicorpus:
			a_s, b_s = single_substitution(As, Bs)
			try:
				a_t, b_t = bidictionary[a_s], bidictionary[b_s]
			except KeyError:
				continue
			else:
				if __verbose__: print >> sys.stderr, '\t{} <--> {}\t{} <--> {}'.format(a_s, b_s, a_t, b_t)
				print '{}\t{}'.format(Bs, bicorpus[As].replace(a_t, b_t))

if __name__ == '__main__':
	options = read_argv()
	__verbose__ = options.verbose
	t1 = time.time()
	translate(
		Bicorpus.fromFile(open(options.corpus), source=options.source, target=options.target),
		Bidictionary.fromFile(open(options.dictionary), source=options.source, target=options.target))
	if __verbose__: print >> sys.stderr, '# Processing time: ' + ('%.2f' % (time.time() - t1)) + 's'
	
	
	
