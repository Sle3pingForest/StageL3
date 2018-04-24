#!/usr/bin/python
# -*- coding: utf-8 -*-

#from __future__ import unicode_literals

import sys
import time
from _fast_distance import fast_distance, fast_similitude, init_memo_fast_distance, memo_fast_distance, memo_fast_similitude

###############################################################################

__author__				= 'Yves Lepage <yves.lepage@waseda.jp>'
__date__, __version__	= '05/02/2016', '1.0'	# Creation.
__description__			= 'Fast computation of distance and similarity between strings.'
__verbose__				= False					# Gives information about timing, etc. to the user.

###############################################################################

def read_argv():

	from optparse import OptionParser
	this_version = 'v%s (c) %s %s' % (__version__, __date__.split('/')[2], __author__)
	this_description = __description__
	this_usage = '''%prog  straingA  stringB
	'''

	parser = OptionParser(version=this_version, description=this_description, usage=this_usage)
	parser.add_option('-v', '--verbose',
						action='store_true', dest='verbose', default=False,
                  		help='run in verbose mode')
						
	(options, args) = parser.parse_args()
	return options, args

###############################################################################

if __name__ == '__main__':
	options, args = read_argv()
	__verbose__ = options.verbose
	t1 = time.time()
	if len(args) != 2:
		print 'Error: two arguments required.'
		sys.exit(-1)
	print fast_distance(args[0], args[1])
	if __verbose__: print >> sys.stderr, '# Processing time: %.2fs' % (time.time() - t1)
