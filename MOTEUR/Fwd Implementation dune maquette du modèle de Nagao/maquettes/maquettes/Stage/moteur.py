#!/usr/bin/python
# coding: utf-8

import sys
import time

from bilingual_data import Bicorpus, Bidictionary
from substitution import single_correction, rememoration_index, dist_inclusion, choice_rememoration_index
from _fast_distance import init_memo_fast_distance, memo_fast_distance

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>, André Giang <andre.giang8@etu.univ-lorraine.fr>'
__date__, __version__ = '06/06/2018', '1.0'
__description__ = '''
	Correct the sentences given on the standard input
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
		
		Ex:
		cat test_rememoration.txt | python moteur.py base_de_cas.txt -s 1 -t 2

		or
		
		printf "J'aime pas nager." | python moteur.py base_de_cas.txt -s 1 -t 2

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

def correct(bicorpus, sentence = False, file=sys.stdin):
	if sentence != False: 
		tab = [sentence]
		file = tab
#	bidictionary = bicorpus
	for Bs in file:
		string = sentence
		Bs = Bs.rstrip('\n')
		if __verbose__: print >> sys.stderr, '\n# Translating sentence: {}'.format(Bs)
#		for As in bicorpus:
		if sentence == False: string = Bs
#		index level
		k = 3
		indice = 0
		indexation = {}
		couple = {}
		for As in bicorpus.iter(string, strategy='by distance', method='direct'):
			init_memo_fast_distance(Bs)
			dist = memo_fast_distance(As[0])
#			Case where the sentence is already in the case base
			if  dist == 0:
				print '{}'.format(As[1])
				sys.exit(0)
			else :	
				a_s, b_s, c_s, e_s, pos, pos_em = single_correction(As[0], Bs, As[1])
				Bt = a_s+b_s+c_s
				dist_cible = memo_fast_distance(Bt)
				if dist_cible != 0:
					phrase = e_s
					indexation[indice,0] = phrase
					couple[indice,0] = As[0]
					couple[indice,1] = As[1]
#					start to 1, 0 is the substring to replace 
					for i in range(1,k):
						phrase = rememoration_index(As[0], phrase, pos_em)
						indexation[indice,i] = phrase
					indice += 1
		if indice > 0:
			result = choice_rememoration_index(Bs, indice, couple, indexation, k)
			a_s, b_s, c_s, e_s, pos, pos_em = single_correction(result[0], Bs, result[1])
			Bt = a_s+b_s+c_s
			print '{}'.format(Bt)
			

if __name__ == '__main__':
	bidata = Bicorpus()
	if len(sys.argv)  == 1:
		phrase = raw_input('Rentrez la phrase à corriger : ')
		choix = raw_input('Voulez vous entrer une correction ? O/n : ')
		if choix == 'O':
			src = raw_input('Rentrez la phrase source fausse : ')
			src_corr = raw_input('Rentrez la phrase source corrigée : ')
			bidata += Bicorpus.fromInput(src,src_corr)
		elif choix == 'n':
			base_de_cas = raw_input('Rentrez le nom de la base de cas à utiliser : ')
			sys.stdin = base_de_cas
			bidata += Bicorpus.fromFile(open(base_de_cas), 0, 1)
		
		correct(bidata, phrase)
	else:	
		options = read_argv()
		__verbose__ = options.verbose
		t1 = time.time()
		for filename in options.training_data:
			bidata += Bicorpus.fromFile(open(filename), source=options.source-1, target=options.target-1) #Bicorpus.fromDb('CASE_BASE')
		correct(bidata)
		if __verbose__: print >> sys.stderr, '# Processing time: ' + ('%.2f' % (time.time() - t1)) + 's'

	
	
	
