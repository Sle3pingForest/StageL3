#!/usr/bin/python
# coding: utf-8

import sys
import time

from bilingual_data import Bicorpus, Bidictionary
from substitution import single_substitution, single_correction, rememoration_index, dist_inclusion
from _fast_distance import init_memo_fast_distance, memo_fast_distance, memo_fast_similitude, fast_distance
from _nlg import solvenlg, verifnlg

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
		commande de base
		Ex: printf "J'aime pas nager." | python Test.py base_de_cas.txt -s 1 -t 2
		
		commande pour site php
		Ex: python Test.py base_de_cas.txt -s 1 -t 2 -se "J'aime pas nager."

		mysql azerty qwerty
		insert into CASE_BASE values (1,'je aimer let pommes', 'j\'aime les pommes','true','e aimer','\'aime',1,1,'fr');
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
	parser.add_argument('-se', '--sentence',
					action='store', type=str, default=3,
					help=source_and_target_help)
	parser.add_argument('-V', '--verbose',
					action='store_true',
					help='verbose mode')

	return parser.parse_args()

################################################################################

def translate(bicorpus, sentence = False, file=sys.stdin):
	"""
	input: Bs, a sentence in the source language
	output: list of Bt, sentences in the target language, candidate translations
	data (passed as arguments):
		bicorpus = list of pairs (As, At) where At is the translation of As.
		bidictionary = bilingual dictionary of (a_s, a_t) where a_s is a word, and a_t its translation.
	"""
	if sentence != False: 
		tab = [sentence]
		file = tab
#	bidictionary = bicorpus
	for Bs in file:
		#compteur de la plus basse distance entre la chaine et les cas dans le dictionnaire
		dist = sys.maxint
		super_dist = sys.maxint
		Bs = Bs.rstrip('\n')
		if __verbose__: print >> sys.stderr, '\n# Translating sentence: {}'.format(Bs)
#		for As in bicorpus:
		string = sentence
		if sentence == False: string = Bs
		# niveau d'index
		k = 6
		indice = 0
		indexation = {}
		couple = {}
		for As in bicorpus.iter(string, strategy='by distance', method='direct'):
			init_memo_fast_distance(Bs)
#			Case where the sentence is already in the case base
			dist = memo_fast_distance(As[0])
			if  dist == 0:
				print '{}\t{}', Bs,'\t',As[1]
				sys.exit(0)
			else :
				a_s, b_s, c_s, e_s, pos, pos_em = single_correction(As[0], Bs, As[1])
				Bt = a_s+b_s+c_s
				dist_cible = memo_fast_distance(Bt)
				print Bt,As[0]
				if dist_cible != 0:
					phrase = e_s
					indexation[indice,0] = phrase
					couple[indice,0] = As[0]
					couple[indice,1] = As[1]
					for i in range(1,k):
						phrase = rememoration_index(As[0], phrase, pos_em)
						indexation[indice,i] = phrase
						"""
						if As[0] == 'Je suis sur Nancy.':
							print phrase, pos_em
						"""
						print phrase
					indice += 1
		#print indexation
		if indice > 0:
			result = [couple[0,0], couple[0,1]]
			index = 0
			for i in range(indice):
				#print couple[i,0]
				trouve = False
				j = 0
				while trouve == False and j < 3:
					d_incA = dist_inclusion(indexation[index,j], Bs) 
					d_incB = dist_inclusion(indexation[i,j], Bs) 
					#print result[0],j, d_incA, d_incB,indexation[index,j], indexation[i,j],'\t', couple[i,0]
					if  j == 2 and d_incA == d_incB:
						init_memo_fast_distance(Bs)
						dist_srcA = memo_fast_distance(couple[index,0])
						dist_srcB = memo_fast_distance(couple[i,0])
						if dist_srcB < dist_srcA:
							result = [couple[i,0], couple[i,1]]
							index = i
					else :
						if d_incB != 0 and d_incA != 0:
							if d_incB < d_incA:
									result = [couple[i,0], couple[i,1]]
									index = i
									trouve = True
							else: 
								if d_incA < d_incB:
									trouve = True
					j += 1
			#print result[0], result[1]
			a_s, b_s, c_s, e_s, pos, pos_em = single_correction(result[0], Bs, result[1])
			Bt = a_s+b_s+c_s
			print '{} : {} :: {} : {}'.format(result[0], result[1],Bs, Bt)
"""
			
			if __verbose__: print >> sys.stderr, '#\t{} : {} : {} :: {} : {} : {}\n'.format(a_s, b_s, c_s, As[0], Bs, As[1])

			#Filtre les cas où il n'y a pas eu de changement lors de la correction
			
			dist_cible = memo_fast_distance(Bt)

			init_memo_fast_distance(result[0])
			dist_src = memo_fast_distance(result[1])
			Dt = solvenlg(result[0], result[1], Bs)	

			print '{}\t{}'.format(Bs, Bt)
			if dist_cible != 0 and Dt != None and verifnlg(result[0], result[1], Bs, Dt):# and dist_cible == dist_src:

				
				print '{}\t{}'.format(Bs, Dt)
				print '{}\t{}'.format(Bs, Bt)
"""
			

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
		
		translate(bidata, phrase)
	else:	
		options = read_argv()
		__verbose__ = options.verbose
		t1 = time.time()
		for filename in options.training_data:
			bidata += Bicorpus.fromFile(open(filename), source=options.source-1, target=options.target-1) #Bicorpus.fromDb('CASE_BASE')  #Bicorpus.fromFile(open(filename), source=options.source-1, target=options.target-1)
		translate(bidata, options.sentence)
		if __verbose__: print >> sys.stderr, '# Processing time: ' + ('%.2f' % (time.time() - t1)) + 's'

	
	
	
