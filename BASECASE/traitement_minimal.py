#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
script qui m'a permis d'ajouter a la fin de chaque ligne du fichier base_de_cas(minimal).txt "fr"

"""

nom="base_de_cas(minimal).txt"
print nom
nom_sorti = "base_de_cas_minimal.csv"
fichier_sorti=open(nom_sorti,"w")
print "creation et ouverture de "+ nom_sorti
with open(nom,"r") as file: #permet de traiter ligne par ligne
    for line in file:
        #print line
        chaine = line
        chaine = chaine.replace("\n", "\tfr\n")
        fichier_sorti.write(chaine)
fichier_sorti.close()


