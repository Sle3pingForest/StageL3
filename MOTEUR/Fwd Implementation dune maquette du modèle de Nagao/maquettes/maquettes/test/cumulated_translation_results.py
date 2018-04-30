#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import collections

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>'
__date__, __version__ = '24/10/2017', '1.0'
__description__ = '''
	Counts the number of time a sentence has been translated in the same way.
'''
__verbose__ = False

################################################################################

def read_argv():

	import argparse
	this_version = 'v%s (c) %s %s' % (__version__, __date__.split('/')[2], __author__)
	this_description = __description__
	this_usage = '''
		%(prog)s  <  input  > output

	For the input:
		As \t At1
		As \t At1
		As \t At2
		
	delivers the output:
		As \t At1 \t 2
		As \t At2 \t 1
	'''

	parser = argparse.ArgumentParser(version=this_version, description=this_description, usage=this_usage)
	parser.add_argument('-V', '--verbose',
					action='store_true',
					help='verbose mode')
	return parser.parse_args()

################################################################################

if __name__ == '__main__':
	options = read_argv()
	__verbose__ = options.verbose
	t1 = time.time()
	d = collections.defaultdict(list)
	for line in sys.stdin:
		As, At = line.rstrip('\n').split('\t')
		d[As].append(At)
	for As in d:
		d[As] = collections.Counter(d[As])
	for As in d:
		for At in d[As]:
			print '{}\t{}\t{}'.format(As, At, d[As][At])
	if __verbose__: print >> sys.stderr, '# Processing time: ' + ('%.2f' % (time.time() - t1)) + 's'
	
	
	
