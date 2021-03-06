#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
from _fast_distance import init_memo_fast_distance, memo_fast_distance

#...!....1....!....2....!....3....!....4....!....5....!....6....!....7....!....8
################################################################################

__author__ = 'Yves Lepage <yves.lepage@waseda.jp>, André Giang <andre.giang8@etu.univ-lorraine.fr>'
__date__, __version__ = '06/06/2018', '1.0'
__description__ = '''
	Module to extract substitutions.
'''
__verbose__ = False

################################################################################

def single_correction(As, Bs, Cs):
	"""
	input: three arguments to resolve analogy equation
		As : Cs :: Bs : x
		As = is source problem
		Cs = correction of Cs
		Bs = current problem we would resolve
	output: three strings to concatenate to obtain solution and some positions for rememoration_index
		Bs prefix 
		modification after to apply
		Bs suffix
		modification before to replace
		position end of prefix
		position modification before
		
	"""

	from os.path import commonprefix
	def longest_commonsuffix(list_of_strings):
		reversed_strings = [' '.join(s.split()[::-1]) for s in list_of_strings]
		reversed_lcs = commonprefix(reversed_strings)
		lcs = ' '.join(reversed_lcs.split()[::-1])
		return lcs

	def commonsuffix(list):
		return commonprefix([s[::-1] for s in list])[::-1]

	pos_souschaine3 = 0
	#prefix suffix between source problem and current problem
	prefix, suffix = commonprefix([Bs, As]), commonsuffix([Bs, As])
	if  len(prefix) > 1:	
		#Case where the beginning is similar
		pos1 = Bs.find(prefix)
		pos2 = Bs.find(suffix)
		sousChaine = Bs[pos1+len(prefix):pos2]	
	else:
		#Case where substring is similar not the beginning
		#utilisation of lcs (longest common substring)
		tab = lcs(As,Bs)
		prefix = ''
		if tab: 
			prefix = tab[len(tab)-1]
		if len(prefix) > 1:
			pos1 = Bs.find( prefix )
			pos2 = len(Bs) -1
			sousChaine = Bs[pos1+len(prefix):pos2]
		else:
			#Case where there are nothing similar
			sousChaine2 = ''
			sousChaine3 = ''
			fin_dep = 0
			pos_souschaine3 = -1

	if __verbose__: print >> sys.stderr, 'prefix/suffix({}, {}) = {}, {}'.format(As, Bs, prefix, suffix)

	if pos_souschaine3 != -1:
		sousChaine2, sousChaine3, fin_dep, pos_souschaine3 = search_prefix_suffix(As,Bs,Cs, prefix, suffix, sousChaine)
		
	deb_fin = fin_dep + len( sousChaine3 )
	debut = 0

	return Bs[debut:fin_dep], sousChaine2, Bs[deb_fin:len(Bs)], sousChaine3, fin_dep, pos_souschaine3

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

def fcs(S,T):
	"""
	first common substring
	"""
	m = len(S)
	n = len(T)
	counter = [[0]*(n+1) for x in range(m+1)]
	longest = 0
	lcs_set = []
	i = 0
	j_avant =  0
	find = False
	while i < m:
		j = 0
		while j < n:
			if S[i] == T[j]:
				c = counter[i][j] + 1
				counter[i+1][j+1] = c
				if c > longest and (j - j_avant) <= 1:
					lcs_set = []
					longest = c
					lcs_set.insert(0,S[i-c+1:i+1])
					find = True
					j_avant = j
			j += 1
		i += 1
	return lcs_set

###############################################################################

def search_prefix_suffix(As,Bs,Cs, prefix, suffix, sousChaine):
	"""
	Search string to replace to correct Bs
	input:
		As = is source problem
		Cs = correction of Cs
		Bs = current problem we would resolve
		prefix = common prefix between As and Bs
		suffix = common suffix between As and Bs
		sousChaine = string in Bs between prefix, suffix
	output:
		sousChaine2 = string to apply to correct sentence
		sousChaine3 = string to replace to correct sentence
		fin_dep = position end of prefix of Bs
		pos_souschaine3 = position of sousChaine3
		
	"""
	from os.path import commonprefix
	def longest_commonsuffix(list_of_strings):
		reversed_strings = [' '.join(s.split()[::-1]) for s in list_of_strings]
		reversed_lcs = commonprefix(reversed_strings)
		lcs = ' '.join(reversed_lcs.split()[::-1])
		return lcs

	def commonsuffix(list):
		return commonprefix([s[::-1] for s in list])[::-1]
	
	tab = {}
	prefix4 = ''
	verif = False
	pos1 = Bs.find(prefix)
	
	tab = fcs(As,Cs)
	if tab: 
		prefix4 = tab[len(tab)-1]
		if len(prefix4) >= len(prefix) and Cs.find(prefix4) <= Cs.find(prefix):
			if Cs.find(prefix) == -1:
				verif = True
	
	#prefix suffix between source solution and source problem
	prefix2, suffix2 = commonprefix([Cs, As]), commonsuffix([Cs, As])
	if verif: prefix2 = prefix4
	pos_prefix2 = Cs.find(prefix2)
	pos_suffix2 = Cs.find(suffix2)
	# souschaine2 = substring which wil replace sousChaine3
	sousChaine2 = Cs[pos_prefix2+len(prefix2):pos_suffix2]
	taille = pos_prefix2+len(prefix2) + len(sousChaine2)
	#position prefix2 in problem to correct
	pos_prefix2_dans_cible = Bs.find(prefix2)

	#prefix suffix between source problem and his solution
	prefix3, suffix3 = commonprefix([As, Cs]), commonsuffix([As, Cs])
	if verif: prefix3 = prefix4
	pos3 = As.find(prefix3)
	pos4 = As.find(suffix3)
	# souschaine3 = substring which will be replace by sousChaine2
	sousChaine3 = As[pos3+len(prefix3):pos4]
	
	#end of prefix
	fin_dep = pos_prefix2_dans_cible+len(prefix2)

	pos_souschaine3 = pos3+len(prefix3)
	
	pos, p, ind = calcul_pos(As, sousChaine3, pos_souschaine3) 

	#search position where to do substitution
	Ps = Bs[0:pos1]
	phrase_index = Ps.split('\'')
	phrase_modif = []
	for i in range(0,len(phrase_index)):
		phrase_modif += phrase_index[i].split(' ')
	word_before = len( phrase_modif)
	i = 0
	t = 0
	while i < word_before:
		if phrase_modif[i] != '':
			t += len(phrase_modif[i])
			#espace
			if t < len(Bs) and Bs[t] == ' ':
				t += 1 
			i += 1
		else:
			word_before -= 1
	phrase_index = Bs.split('\'')
	phrase_modif = []
	for m in range(0,len(phrase_index)):
		phrase_modif += phrase_index[m].split(' ')
	j = i
	fin = i + ind
	if fin <= len ( phrase_modif ):
		for j in range(j,fin):
			t += len(phrase_modif[j])
			taille = pos1 + pos + len( sousChaine3 )
			if t < len(Bs) and Bs[t] == ' ':
				t += 1 
		fin_dep = t + pos


	"""
	if  As == 'J\'adore pas les pommes.' :#or As == 'Je tues.' or As == 'C\'est de la faute de sa femme.':
		
		print pos, p , ind
		print '\n 1er' , prefix, '|' ,  sousChaine ,'|' , suffix
		print As ,' je suis dans le suffixe ', Cs #, As.split(suffix, len(As) - len(prefix)) , '\n'
		print ' 2 Correction' ,len(Cs), '| Prefix', pos_prefix2, '|', len(prefix2),'| Suffix',pos_suffix2, '|', len(suffix2) , '| Mid',len(sousChaine2), '\n'
		print '  2eme ', prefix2, '|' ,  sousChaine2 ,'|' , suffix2,'\n'
		print ' 3 Correction' ,len(As), '| Prefix', pos3, '|', len(prefix3),'| Suffix',pos4, '|', len(suffix3) , '| Mid',len(sousChaine3), '\n'
		print '  3eme ', prefix3, '|' ,  sousChaine3 ,'|' , suffix3,'\n'
		print '  3eme ',As, pos_prefix2 ,  len(prefix2) ,  taille
		print ' 4eme ',As[pos_prefix2:pos_prefix2+len(prefix2)],  As[taille:len(As)]
		print Bs[0:fin_dep] , '|', sousChaine2, '|', Bs[fin_dep+len(sousChaine3):len(Bs)]
		print 'fin_dep',fin_dep, 'dep_fin', fin_dep+len(sousChaine3)
	"""
	
	return sousChaine2, sousChaine3, fin_dep, pos_souschaine3

############################################################################

def rememoration_index(Ds, empreinte, pos_em_Ds):
	"""
	Retrieve 1 word to the right and to the left of the string empreinte
	>>> rememoration_index('Je n'aime pas nager', 'e n', 1)
	('Je n'aime')
	>>> rememoration_index('Je suis à Metz', 'à ', 9)
	('suis à Metz')
	>>> rememoration_index('J'aime pas les maths et l'algèbre', 'è', 9)
	('l'algèbre')
	"""
	pos, split, indice = calcul_pos(Ds, empreinte,pos_em_Ds)
	avant = ''
	phrase = ''
	apres = ''
	indice_avant = indice - 1
	indice_apres = indice + 1
	if pos != -1:
		taille_em = len(empreinte)
		taille_split = len(split)
		phrase = split[indice]
		if taille_em == len(phrase) or empreinte == '':
			if indice_avant >= 0 : avant = split[indice_avant]
			if indice_apres < len(split) : apres = split[indice_apres] 
			phrase = avant + ' ' + empreinte + ' ' + apres
		else:
			while len(phrase) <= taille_em and len(phrase) < len(Ds):
				if indice_apres < taille_split:
					apres = ' ' + split[indice_apres]
					indice_apres += 1
				else :
					apres = ''
				if indice_avant >= 0:
					avant = split[indice_avant] + ' '
					indice_avant -= 1
				else :
					avant = ''
				phrase = avant + phrase + apres
	
	return phrase

############################################################################

def calcul_pos(phrase, empreinte, position):
	"""
	input:
		phrase = sentence
		empreinte = substring in sentence
		position = position of empreinte
	output:
		phrase_modif = split of all word 
		i = index of the word where there is the substitution
		pos_em = position of empreinte in the word where the substitution begin
	"""
	phrase_index = phrase.split('\'')
	phrase_modif = []
	for i in range(0,len(phrase_index)):
		phrase_modif += phrase_index[i].split(' ')
	i=0
	taille = len(phrase_modif)
	t = 0
	trouve = False
	pos_em = -1
	pos = phrase.find(empreinte)
	while i < taille and trouve == False:	
		t += len( phrase_modif[i])
		if t >= position:
			pos_em = phrase_modif[i].find(empreinte)		
			pos_em = position - (t - len( phrase_modif[i]) )	
			if pos_em != -1:
				trouve = True

		#add a space
		t += 1
		i += 1		

	if trouve == True: i -= 1
	else :
		if trouve == False and pos == -1: 
			i = -1

	return pos_em, phrase_modif, i
		

################################################################################

def lcs(S,T):
	"""
	longest common substring
	lcs('I love eat something good', I lose every fight i do.') = 'I lo'
	"""
	m = len(S)
	n = len(T)
	counter = [[0]*(n+1) for x in range(m+1)]
	longest = 0
	lcs_set = []
	for i in range(m):
		for j in range(n):
		    if S[i] == T[j]:
			c = counter[i][j] + 1
			counter[i+1][j+1] = c
			if c > longest:
			    lcs_set = []
			    longest = c
			    lcs_set.insert(0,S[i-c+1:i+1])
			elif c == longest:
			    lcs_set.insert(0,S[i-c+1:i+1])

	return lcs_set

################################################################################

def dist_inclusion(phrase_index, probleme):
	"""
	input:
		phrase_index = words around the substring to replace and the substring in source problem
		probleme = problem we want to correct
	output:
		return number of word that's not in problem
	"""
	compteur = 0
	if phrase_index != '':
		phrase_index = phrase_index.split('\'')
		phrase_modif = []
		for i in range(0,len(phrase_index)):
			phrase_modif += phrase_index[i].split(' ')
		for i in range( len(phrase_modif) ):
			if probleme.find(phrase_modif[i]) == -1:
				compteur += 1
		compteur += 1
	return compteur

################################################################################

def choice_rememoration_index(Bs, indice, couple, indexation, k):
	"""
	input: 
		Bs = sentence to correct
		indice = size of elements to compare
		couple = source problem and his solution
		indexation = list of string get by method rememoration_index
		k = index level
	output: chosen couple to apply correction
	"""
	#search and return the best case with index rememoration
	result = [couple[0,0], couple[0,1]]
	index = 0
	for i in range(indice):
		trouve = False
		j = 0
		while trouve == False and j < k:
			d_incA = dist_inclusion(indexation[index,j], Bs) 
			d_incB = dist_inclusion(indexation[i,j], Bs) 
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
	return result

################################################################################

def base_case_param(As,Cs):
	"""
	Get information to insert in database table CASES
	output:
		modification before/after + position
	"""
	from os.path import commonprefix
	def longest_commonsuffix(list_of_strings):
		reversed_strings = [' '.join(s.split()[::-1]) for s in list_of_strings]
		reversed_lcs = commonprefix(reversed_strings)
		lcs = ' '.join(reversed_lcs.split()[::-1])
		return lcs

	def commonsuffix(list):
		return commonprefix([s[::-1] for s in list])[::-1]


	#prefix suffix between source problem and origin problem 
	prefix, suffix = commonprefix([As, Cs]), commonsuffix([As, Cs])
	
	pos_prefix1 = As.find(prefix)
	pos_suffix1 = As.find(suffix)
	# souschaine3 = substring which will be replace by sousChaine2
	sousChaine = As[pos_prefix1+len(prefix):pos_suffix1]


	#prefix suffix between source solution and source problem
	prefix2, suffix2 = commonprefix([Cs, As]), commonsuffix([Cs, As])
	pos_prefix2 = Cs.find(prefix2)
	pos_suffix2 = Cs.find(suffix2)
	# souschaine2 = substring which wil replace sousChaine3
	sousChaine2 = Cs[pos_prefix2+len(prefix2):pos_suffix2]


	pos_souschaine = pos_prefix1+len(prefix)

	return sousChaine, sousChaine2,  pos_souschaine

	
