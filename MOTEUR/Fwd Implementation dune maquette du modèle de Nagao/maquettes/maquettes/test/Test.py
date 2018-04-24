#!/usr/bin/python
# coding: utf-8

import sys
import time

from bilingual_data import Bicorpus, Bidictionary
from substitution import single_substitution
from _fast_distance import init_memo_fast_distance, memo_fast_distance, memo_fast_similitude, fast_distance

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>'
__date__, __version__ = '18/04/2018', '1.1'
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
		%(prog)s  CORPUS

		Ex: printf "J'aime pas les pommes" | python Test.py base_de_cas.txt -s 1 -t 2
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
	input: Bs, a sentence in the source language
	output: list of Bt, sentences in the target language, candidate translations
	data (passed as arguments):
		bicorpus = list of pairs (As, At) where At is the translation of As.
		bidictionary = bilingual dictionary of (a_s, a_t) where a_s is a word, and a_t its translation.
	"""
#	bidictionary = bicorpus
	for Bs in file:
		#compteur de la plus basse distance entre la chaine et les cas dans le dictionnaire
		dist = sys.maxint;
		Bs = Bs.rstrip('\n')
		if __verbose__: print >> sys.stderr, '\n# Translating sentence: {}'.format(Bs)
#		for As in bicorpus:
		for As in bicorpus.iter(string=Bs, strategy='by distance', method='direct'):
			#print As
			init_memo_fast_distance(Bs)
#			Case where the sentence is already in the case base
			if dist > memo_fast_distance(As[0]): 
				dist = memo_fast_distance(As[0])
				if  dist == 0:
					print Bs,'\t',As[1]

				else :
					a_s, b_s, c_s = single_substitution(As[0], Bs, As[1])
					#print(As + ' | ' + Bs + '        ' +  a_s + ' | ' + b_s + '\n')
					"""try:
						print 'jesuisalafin', bicorpus[a_s] , bicorpus[b_s]
						a_t, b_t = bicorpus[a_s], bicorpus[b_s]
						#print(a_t + ' | ' + b_t + '        ' +  a_s + ' | ' + b_s + '\n')
					except KeyError:
						continue
					else:
					"""
					if __verbose__: print >> sys.stderr, '#\t{} : {} :: {} : {}\n'.format(a_s, a_t, b_s, b_t)
					print '{}\t{}'.format(Bs, a_s+b_s+c_s)

if __name__ == '__main__':
	options = read_argv()
	__verbose__ = options.verbose
	t1 = time.time()
	bidata = Bicorpus()
	for filename in options.training_data:
		print filename
		bidata += Bicorpus.fromFile(open(filename), source=options.source-1, target=options.target-1)
	translate(bidata)
	if __verbose__: print >> sys.stderr, '# Processing time: ' + ('%.2f' % (time.time() - t1)) + 's'
	
	
	
