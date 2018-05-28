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

def single_correction(As, Bs, Cs):

	from os.path import commonprefix
	def longest_commonsuffix(list_of_strings):
		reversed_strings = [' '.join(s.split()[::-1]) for s in list_of_strings]
		reversed_lcs = commonprefix(reversed_strings)
		lcs = ' '.join(reversed_lcs.split()[::-1])
		return lcs

	def commonsuffix(list):
		return commonprefix([s[::-1] for s in list])[::-1]


	#prefix suffix entre le probleme source et probleme cible
	prefix, suffix = commonprefix([Bs, As]), commonsuffix([Bs, As])
	verif = False
	if  len(prefix) > 1 or len(suffix) > 1:	
	#Cas ou il y a un debut ou une fin qui ressemble
		pos1 = Bs.find(prefix)
		pos2 = Bs.find(suffix)
		#extraction sans le '/a'
		sousChaine = Bs[pos1+len(prefix):pos2]

		prefix2, suffix2, sousChaine2, prefix3, suffix3, sousChaine3, pos_prefix2_dans_cible, fin_dep, verif, pos = calcul_prefix_suffix(As,Bs,Cs, prefix, suffix, sousChaine)

		#chaine "corrigee"
		if pos_prefix2_dans_cible == -1:
			fin_dep = len(sousChaine)
			#avoir l'espace manquant
			if len(sousChaine.split(' ')) > 1: fin_dep += 1

		#Cas d une suppression de caractere donc quand la souschaine2 est vide
		#Je suppose que cest toujours la fin du mot qui est supprimee
		if sousChaine2 == "" or Cs.split('.')[0] == sousChaine2:
			tab = lcs(As,Bs)
			prefix = tab[len(tab)-1]
			pos1 = Bs.find( prefix )
			pos2 = len(Bs) -1
			sousChaine = Bs[pos1+len(prefix):pos2]

			
			fin_dep, sousChaine3 = suppr_char(As,Bs,pos1,prefix,sousChaine, suffix, prefix2, prefix3, sousChaine3, fin_dep)
			verif = False

			
	else:
		"""
		Cas ou une string ressemble dans la chaine mais ne commence et ne finit pas comme la phrase cible
		utilisation de la distance lcs (longest common string)
		"""
		tab = lcs(As,Bs)
		prefix = ''
		if tab: prefix = tab[len(tab)-1]
		if len(prefix) > 1:
			pos1 = Bs.find( prefix )
			pos2 = len(Bs) -1
			#extraction sans le '/a'
			sousChaine = Bs[pos1+len(prefix):pos2]

			prefix2, suffix2, sousChaine2, prefix3, suffix3, sousChaine3, pos_prefix2_dans_cible, fin_dep, verif, pos = calcul_prefix_suffix(As,Bs,Cs, prefix, suffix, sousChaine)
			#print As,prefix, len(prefix)
			#cas ou la modif est dans le prefix de Bs
			if pos_prefix2_dans_cible == -1:
				pos_dans_Bs = Bs.find(sousChaine3)
				fin_dep = pos_dans_Bs

				#insertion travailler sur taille mot
				if sousChaine3 == '' or sousChaine3 == ' ':
					coupe = As[As.find(prefix2):As.find(prefix2)+ len(prefix2)]
					tableau_prefi = coupe.split(' ')
					tableau_Bs = Bs.split(' ')
					if len(tableau_prefi) <= len(tableau_Bs):
						taille = 0
						tableau_As = As.split(' ')
						for i in range(0,len(tableau_prefi)):
							if tableau_prefi[i] != '':
								taille += len(tableau_Bs[i])
								if tableau_prefi[i] == tableau_As[i]:
									taille += 1
						fin_dep = taille
						verif = False
			
			#Cas d une suppression de caractere donc quand la souschaine2 est vide
			#Je suppose que cest toujours la fin du mot qui est supprimee
			if sousChaine2 == "":
				fin_dep, sousChaine3 = suppr_char(As,Bs,pos1,prefix,sousChaine, suffix, prefix2, prefix3, sousChaine3, fin_dep)
				verif = False

		else:

			#Cas où il n'y a aucune ressemblance retourne la meme chaine
			prefix3 = ''
			prefix2 = ''
			sousChaine2 = ''
			pos_prefix2_dans_cible = 0
			sousChaine3 = ''
			fin_dep =0
			pos = -1

	if __verbose__: print >> sys.stderr, 'prefix/suffix({}, {}) = {}, {}'.format(As, Bs, prefix, suffix)


	debut = 0
	if verif:
		index = As.find(prefix3)
		if index != -1:
			debut = index
			fin_dep = debut + len(prefix3.decode('utf-8'))


	# borne de debut du suffix
	deb_fin = fin_dep+len(sousChaine3)
	if deb_fin > len(Bs) and fin_dep < len(Bs): 
		deb_fin = fin_dep

	"""
	point a checker	
	print ' AAAAAAAAAAAAAAAAAAAAAAAAAAA ', As[len(prefix):-len(suffix)], Bs[len(prefix):-len(suffix)]
	"""

	return Bs[debut:fin_dep], sousChaine2, Bs[deb_fin:len(Bs)], sousChaine3, fin_dep, pos

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

def calcul_prefix_suffix(As,Bs,Cs, prefix, suffix, sousChaine):
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
	
	tab = fcs(As,Cs)
	if tab: 
		prefix4 = tab[len(tab)-1]
		if len(prefix4) >= len(prefix) and Cs.find(prefix4) <= Cs.find(prefix):
			if Cs.find(prefix) == -1:
				verif = True
	
	#prefix suffix entre la solution du probleme source et le probleme dans la solution
	prefix2, suffix2 = commonprefix([Cs, As]), commonsuffix([Cs, As])
	if verif: prefix2 = prefix4
	pos_prefix2 = Cs.find(prefix2)
	pos_suffix2 = Cs.find(suffix2)
	# souschaine2 = chaine qui remplace qui se trouve entre le prefix et le suffixe
	sousChaine2 = Cs[pos_prefix2+len(prefix2):pos_suffix2]

	taille = pos_prefix2+len(prefix2) + len(sousChaine2)

	#position du prefix2 dans le probleme cible
	pos_prefix2_dans_cible = Bs.find(prefix2)

	#prefix suffix entre le probleme source et sa solution dans le src
	prefix3, suffix3 = commonprefix([As, Cs]), commonsuffix([As, Cs])
	if verif: prefix3 = prefix4
	#if As == 'Inné.':
	#print As,Cs,prefix3, sousChaine2
	pos3 = As.find(prefix3)
	pos4 = As.find(suffix3)
	# souschaine3 = chaine qui va etre remplacer par la souschaine 2
	sousChaine3 = As[pos3+len(prefix3):pos4]
	#print prefix3,sousChaine3,suffix3
	
	#borne de fin de prefix
	fin_dep = pos_prefix2_dans_cible+len(prefix2)

	taille = pos3+len(prefix3)
	
	pos, p, ind = calcul_pos(As, sousChaine3, taille) 

	"""
	if  As == 'Je m\'arete.' :#or As == 'Je tues.' or As == 'C\'est de la faute de sa femme.':
		
		print '\n 1er' , prefix, '|' ,  sousChaine ,'|' , suffix
		print As ,' je suis dans le suffixe ', Cs #, As.split(suffix, len(As) - len(prefix)) , '\n'
		print ' 2 Correction' ,len(Cs), '| Prefix', pos_prefix2, '|', len(prefix2),'| Suffix',pos_suffix2, '|', len(suffix2) , '| Mid',len(sousChaine2), '\n'
		print '  2eme ', prefix2, '|' ,  sousChaine2 ,'|' , suffix2,'\n'
		print ' 3 Correction' ,len(As), '| Prefix', pos3, '|', len(prefix3),'| Suffix',pos4, '|', len(suffix3) , '| Mid',len(sousChaine3), '\n'
		print '  3eme ', prefix3, '|' ,  sousChaine3 ,'|' , suffix3,'\n'
		print '  3eme ',As, pos_prefix2 ,  len(prefix2) ,  taille
		print ' 4eme ',As[pos_prefix2:pos_prefix2+len(prefix2)],  As[taille:len(As)]
		print Bs[0:fin_dep] , '|', sousChaine2, '|', Bs[fin_dep+len(sousChaine3):len(Bs)]
	"""
	return prefix2, suffix2, sousChaine2, prefix3, suffix3, sousChaine3, pos_prefix2_dans_cible, fin_dep, verif, taille

############################################################################

def rememoration_index(Ds, empreinte, pos_em_Ds):

	"""
	Récupère les mots a une distance de 1 a gauche et a droite de l'empreinte
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
		#print empreinte,taille_em, Ds
		if taille_em == len(phrase):
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

	#print avant + '|' + phrase + '|' + apres + '|' + empreinte
	
	return phrase
	

############################################################################

def suppr_char(As,Bs,pos1,prefix,sousChaine, suffix, prefix2, prefix3, sousChaine3,fin_dep):
	fin_dep
	#Calcul i eme mot modifie
	phrase_modif = prefix3 + sousChaine3
	phrase_modif = phrase_modif.split(' ')

	#numero du mot qui est modifie
	taille_pm = len( phrase_modif )

	phrase_modif2 = prefix+sousChaine
	phrase_modif2 = phrase_modif2.split(' ')

	#Si le bout de phrase cible est aussi grand ou plus que la phrase source
	if len( phrase_modif2) >= taille_pm:
		#calcul de la diff entre la phrase source et sa correction : nombre de caractere a supprime
		diff = len(prefix3 + sousChaine3) - len(prefix2) 

		#taille de la chaine quon supprimera par la fin
		t=0
		for x in range(0,taille_pm):
			t+=len(phrase_modif2[x])

		#ajout des espaces entre chaque mot
		t += taille_pm-1
		
		fin_dep = pos1 + t- diff


		phrase_modif2 = prefix+sousChaine+suffix
		phrase_modif2 = phrase_modif2.split(' ')

		#if taille_pm < len(phrase_modif2): sousChaine3 += ' '

	return fin_dep, sousChaine3


############################################################################

def calcul_pos(phrase, empreinte, position):
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
		
		#ajout de lespace
		t += 1
		i += 1		
	if trouve == False and pos == -1: i = -1
	"""
	if  pos != -1 and trouve == False:
		t = 0
		i = 0
		while i < taille and trouve == False:	
			t += len( phrase_modif[i])
	"""
	if trouve == True: i -= 1

	return pos_em, phrase_modif, i
		


################################################################################

def lcs(S,T):
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
