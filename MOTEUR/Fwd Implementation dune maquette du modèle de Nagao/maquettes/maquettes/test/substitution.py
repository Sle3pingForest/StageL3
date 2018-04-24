#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>'
__date__, __version__ = '10/10/2017', '1.0'
__description__ = '''
	Module to extract substitutions.
'''
__verbose__ = False

################################################################################

def single_substitution(As, Bs):
	"""
	Extract a single substitution between two strings.
	>>> single_substitution('this is an example', 'that is an example')
	('is', 'at')
	>>> single_substitution('Well, this is an example', 'Well, that is an example')
	('is', 'at')
	>>> single_substitution('I love apples.', 'They love apples.')
	('I', 'They')
	"""
	from os.path import commonprefix

	def commonsuffix(list):
		return commonprefix([s[::-1] for s in list])[::-1]
	prefix, suffix = commonprefix([As, Bs]), commonsuffix([As, Bs])
	#print As , '     ' , Bs ,  '   ' , prefix , ' sufff  ' , suffix
	if len(prefix) > 0 or len(suffix) > 1:
		pos1 = As.find(prefix)
		pos2 = As.find(suffix)
		#extraction sans le '/a'
		sousChaine = As[pos1+len(prefix):pos2]
		print prefix, '    |    ' ,  sousChaine ,'     |     ' , suffix, '\n'
		#print As ,' je suis dans le suffixe ', As.split(suffix, len(As) - len(prefix)) , '\n'
		print As[len(prefix):-len(suffix)], Bs[len(prefix):-len(suffix)]
	if __verbose__: print >> sys.stderr, 'prefix/suffix({}, {}) = {}, {}'.format(As, Bs, prefix, suffix)
	
	return As[len(prefix):-len(suffix)], Bs[len(prefix):-len(suffix)]

################################################################################

def single_substitution(As, Bs, Cs):
	"""
	Extract a single substitution between two strings.
	>>> single_substitution('this is an example', 'that is an example')
	('is', 'at')
	>>> single_substitution('Well, this is an example', 'Well, that is an example')
	('is', 'at')
	>>> single_substitution('I love apples.', 'They love apples.')
	('I', 'They')
	"""
	from os.path import commonprefix
	def commonsuffix(list):
		return commonprefix([s[::-1] for s in list])[::-1]

	#prefix suffix entre le probleme source et probleme cible
	prefix, suffix = commonprefix([As, Bs]), commonsuffix([As, Bs])


	#si il y a un debut qui ressemble ou une fin qui ressemble
	if 1:#len(prefix) > 0 or len(suffix) > 1:
	
		
		pos1 = As.find(prefix)
		pos2 = As.find(suffix)
		#extraction sans le '/a'
		sousChaine = As[pos1+len(prefix):pos2]
		

		#prefix suffix entre le probleme source et sa solution
		prefix2, suffix2 = commonprefix([Cs, As]), commonsuffix([Cs, As])
		
		pos11 = Cs.find(prefix2)
		pos22 = Cs.find(suffix2)
		#print Cs[pos11],Cs[pos22]
		# souschaine2 = bout qui remplace
		sousChaine2 = Cs[pos11+len(prefix2):pos22]





		taille = pos11+len(prefix2) + len(sousChaine2)
		pos111 = Bs.find(prefix2)
		#Tu veux du poulet va chez Dior et je t'aime pas.
		
		#chaine "corrigee"
		Fs = Bs[0:pos111+len(prefix2)] + sousChaine2 + Bs[pos111+len(prefix2):len(Bs)]


		prefix3, suffix3 = commonprefix([As, Cs]), commonsuffix([As, Cs])

		pos3 = As.find(prefix3)
		pos4 = As.find(suffix3)
		# souschaine2 = bout qui remplace
		sousChaine3 = As[pos3+len(prefix3):pos4]
		#print prefix3,sousChaine3,suffix3

		"""
		print '\n 1er' , prefix, '|' ,  sousChaine ,'|' , suffix
		print As ,' je suis dans le suffixe ', As.split(suffix, len(As) - len(prefix)) , '\n'
		print ' 2 ' ,len(Cs), '|', pos1, '|',pos22, '|', len(prefix2),'|',len(sousChaine2), '|', len(suffix2) , '\n'
		print '  2eme ', prefix2, '|' ,  sousChaine2 ,'|' , suffix2,'\n'


		print '  3eme ',As, pos11 ,  len(prefix2) ,  taille
		print ' 4eme ',As[pos11:pos11+len(prefix2)],  As[taille:len(As)]
		print Bs[0:pos111+len(prefix2)] , '|', sousChaine2, '|', Bs[pos111+len(prefix2)+len(sousChaine3):len(Bs)]
		"""
		

	else:
		prefix2 = ''
		sousChaine2 = ''
		pos111 = 0
		sousChaine3 = ''


		



	if __verbose__: print >> sys.stderr, 'prefix/suffix({}, {}) = {}, {}'.format(As, Bs, prefix, suffix)
	return Bs[0:pos111+len(prefix2)], sousChaine2, Bs[pos111+len(prefix2)+len(sousChaine3):len(Bs)]

################################################################################

def tree_substitution(As, Bs):
	"""
	Extract a tree of substitutions which are possible between two strings As and Bs.
	For that recursively compute the longest common substrings (not subsequences).
	In fact, same as CharCut.
	NOT IMPLEMENTED.
	"""
	return None

################################################################################

def lcs(S,T):
    m = len(S)
    n = len(T)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    lcs_set = set()
    for i in range(m):
        for j in range(n):
            if S[i] == T[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(S[i-c+1:i+1])
                elif c == longest:
                    lcs_set.add(S[i-c+1:i+1])

    return lcs_set

