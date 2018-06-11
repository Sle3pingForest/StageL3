#!/usr/bin/python
# coding: utf-8

import sys
import time

from bilingual_data import Bicorpus, Bidictionary
from _nlg import solvenlg, verifnlg

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>'
__date__, __version__ = '24/10/2017', '1.0'
__description__ = '''
	Translates the sentences given on the standard input
	using Lepage's indirect model of translation by analogy.
	For that, uses the bicorpus
	passed as positional argument.
'''
__verbose__ = False

################################################################################

def lengths(source, target):
	terms = [source, target]
	terms = zip(*terms)
	return (max(len(source.decode('utf8')), len(target.decode('utf8'))) for (source, target) in terms)

################################################################################

def read_argv():

	import argparse
	this_version = 'v%s (c) %s %s' % (__version__, __date__.split('/')[2], __author__)
	this_description = __description__
	this_usage = '''
		%(prog)s  CORPUS
		
		Ex: cat EBMT_test.txt | cut -f 2 | indirect_model.py EBMT_corpus.txt EBMT_dictionary.txt -s 2 -t 5
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

nlg_fmt = '{:^{lA}} : {:^{lB}} :: {:^{lC}} : {:^{lD}}'
two_line_nlg_fmt = '\n# {}\n# {}'.format(nlg_fmt, nlg_fmt)

def translate(bicorpus, file=sys.stdin):
	"""
	input: Ds in the source language
	output: list of Bt in the target language, candidate translations
	data (passed as argument):
		bicorpus = list of pairs (As, At) where At is the translation of As.
	"""
	for Ds in file:
		Ds = Ds.rstrip('\n')
		if __verbose__: print >> sys.stderr, '\n# Translating sentence: {}'.format(Ds)
#		import itertools
#		for (As, Bs, Cs) in itertools.product(bicorpus, repeat=3):
		for (As, Bs, Cs) in bicorpus.iter(string=Ds, strategy='closest', method='indirect'):
			if Ds == Bs:
				print '{}\t{}'.format(Ds, bicorpus[Bs])
			else:
				if verifnlg(As, Bs, Cs, Ds):
					At, Bt, Ct = bicorpus[As], bicorpus[Bs], bicorpus[Cs]
					Dt = solvenlg(At, Bt, Ct)
					lA, lB, lC, lD = lengths([As, Bs, Cs, Ds], [At, Bt, Ct, Dt])
					if __verbose__: print >> sys.stderr, \
						('{}  =>  x = {}\n'.format(two_line_nlg_fmt, Dt)).\
							format(As, Bs, Cs, Ds, At, Bt, Ct, 'x', lA=lA, lB=lB, lC=lC, lD=lD)
					print '{}\t{}'.format(Ds, Dt)

if __name__ == '__main__':
	options = read_argv()
	__verbose__ = options.verbose
	t1 = time.time()
	bidata = Bicorpus()
	for filename in options.training_data:
		bidata += Bicorpus.fromFile(open(filename), source=options.source-1, target=options.target-1)
	translate(bidata)
	if __verbose__: print >> sys.stderr, '# Processing time: ' + ('%.2f' % (time.time() - t1)) + 's'

