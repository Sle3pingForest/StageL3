#!/usr/bin/env python
#-*- coding: utf-8 -*-


import xml.etree.ElementTree as etree #bibliothèque compatible python 2.*

#class qui traite le fichier xml adapté à WiKoPaCo
class Treatment_xml:
    def __init__(self,file_XML):
        self.tree=etree.parse(file_XML)
        print "created tree"

    def get_root(self):
        #return l'element racine du fichier xml
        root_element = "root element : "
        root_element = root_element + self.tree.getroot().tag
        print root_element
        return self.tree.getroot()

    def get_terms(self):
        #permettra de gerer les filtres
        return True

    #processing to cvs file
    def treatment_cvs(self):
        #print "treatment"
        nom ="base_de_cas_WiKoPaCo.csv"
        fichier_txt = open(nom,"w")#ouverture en ecriture avec ecrasement
        print "file "+nom+" open"
        #racine du fichier xml
        root = self.get_root()
        #compteur du nombre de cas traité
        compteur = 0
        nb_cas=0
        #acces aux balises <modif>
        for modif in root:
            #filtre des cas
            if(self.get_terms()):
                nb_cas+=1
                compteur+=1
                #gestion des balises <before> et <after>
                for cas in modif:
                    chaine = cas.text
                    #print cas.tag #affiche le nom de la balise
                    #gestion de balise <m> qui correspond a la modification effectuée
                    for m in cas :
                        chaine = chaine + m.text
                        #print m.text #affiche ce qui est présent a l'interieur de la balise m
                        if(cas.tag=='before'):
                            m_before=m.text
                            #print "m_before"
                        elif(cas.tag=='after'):
                            m_after=m.text
                            #print "m_after"
                        balise_m=etree.tostring(m,encoding='utf8').decode('utf8') #balise <m>
                        compteur = len(balise_m)-1
                        bal_m_modifie=""
                        while(balise_m[compteur]!=">"):
                            bal_m_modifie=balise_m[compteur]+bal_m_modifie
                            compteur=compteur-1
                        chaine=chaine + bal_m_modifie
                        chaine = chaine.strip() #suppr les espace avant et après le string
                        chaine = chaine + "\t"
                        fichier_txt.write(chaine.encode('utf8'))
            fichier_txt.write("True\t".encode('utf8')) #statue de la correction par defaut True
            fichier_txt.write(m_before.encode('utf8')) #avant la correction
            fichier_txt.write("\t".encode('utf8'))
            fichier_txt.write(m_after.encode('utf8')) #après la correction
            fichier_txt.write("\t".encode('utf8'))
            fichier_txt.write("0\t".encode('utf8')) #indice erreur mis a 0 pour tester , A MODIFIER!!!
            fichier_txt.write("corpus WiKoPaCo .\t".encode('utf8')) #source
            fichier_txt.write("fr\n".encode('utf8')) #langue

        fichier_txt.close()
        print "file "+nom+" close"
        print "-------"
        
        print("nombre d'element traité ="),
        print(nb_cas)
        
######### TEST ##############
test = Treatment_xml('wikopaco.xml')
test.treatment_cvs()
        
        
        
        
