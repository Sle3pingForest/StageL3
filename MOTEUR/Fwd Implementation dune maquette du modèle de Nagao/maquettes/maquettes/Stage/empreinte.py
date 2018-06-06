#!/usr/bin/python
# coding: utf-8

import sys
import time

from bilingual_data import Bicorpus, Bidictionary
from substitution import base_case_param
from _fast_distance import init_memo_fast_distance, memo_fast_distance, memo_fast_similitude, fast_distance

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>, André Giang <andre.giang8@etu.univ-lorraine.fr>'
__date__, __version__ = '06/06/2018', '1.0'
__description__ = '''
	Get substitution (before, after, position) of the couple (problem,solution) given on the standard input
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
		%(prog)s  CORPUS

		Ex: python empreinte.py base_de_cas.txt -s 1 -t 2
	'''

	parser = argparse.ArgumentParser(version=this_version, description=this_description, usage=this_usage)
	corpus_and_dictionary_help = 'the bi- or multi-lingual %(metavar)s (see options -s and -t)'
	parser.add_argument('training_data', metavar='TRAINING_DATA', nargs='+',
					action='store', default=None,
					help=corpus_and_dictionary_help)
	source_and_target_help = 'column of the %(dest)s language in the corpus and the dictionary (starts at 1, default: %(default)d)'
	parser.add_argument('-s', '--source',
					action='store', type=int, default=1,
					help=source_and_target_help)
	parser.add_argument('-t', '--target',
					action='store', type=int, default=2,
					help=source_and_target_help)
	parser.add_argument('-V', '--verbose',
					action='store_true',
					help='verbose mode')

	return parser.parse_args()

################################################################################

def translate(bicorpus, file=sys.stdin):
	"""
	output: problem, solution, substitution before,after and his position in the string
	data (passed as arguments):
		bicorpus = list of pairs (As, At) where At is the correction of As.
		bidictionary = bilingual dictionary of (a_s, a_t) where a_s is a sentence, and a_t its correction.
	"""
	for As in bicorpus.iter('', strategy='naive', method='direct'):
		a_s, b_s, pos = base_case_param(As[0], As[1])
		if __verbose__: print >> sys.stderr, '#\t{} : {} : {} :: {} : {}\n'.format(a_s, b_s, c_s, As[0], As[1])

		print '{}\t{}\t{}\t{}\t{}'.format(As[0], As[1], a_s, b_s, pos, )

if __name__ == '__main__':
	bidata = Bicorpus()
	options = read_argv()
	__verbose__ = options.verbose
	t1 = time.time()
	for filename in options.training_data:
		bidata += Bicorpus.fromFile(open(filename), source=options.source-1, target=options.target-1)
	translate(bidata)
	if __verbose__: print >> sys.stderr, '# Processing time: ' + ('%.2f' % (time.time() - t1)) + 's'

	
	
	
