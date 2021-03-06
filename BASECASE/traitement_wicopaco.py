#!/usr/bin/env python
#-*- coding: utf-8 -*-


import xml.etree.ElementTree as etree #bibliothèque compatible python 2.*

#class qui traite le fichier xml adapté à WiCoPaCo
class Treatment_xml:
    '''
    constructeur qui parse le fichier XML donné
    '''
    def __init__(self,file_XML):
        self.tree=etree.parse(file_XML)
        print "created tree"

    '''
    fonction qui returne l'element racine du fichier XML
    '''
    def get_root(self):
        root_element = "root element : "
        root_element = root_element + self.tree.getroot().tag
        print root_element
        return self.tree.getroot()

    def get_terms(self):
        #permettra de gerer les filtres
        return True

    def deleting_correction_duplicate(self,nom,root):
        #permet de supprimer les modifications faite puis remise a l'etat initial (fonctionne sur le fichier wicopaco.xml)
        print("deleting_correction_duplicate")
        compteur = 0
        taille_root = len(root)
        for i in range(0,taille_root):
            if(i%1000==0):
                print i #affiche le compteur régulièrement afin d'avoir une idée de ce qui est deja traité
            #print taille_root
            #print i
            if(taille_root<=i):
                print "break"
                break
            before_id = root[i].get('wp_before_rev_id')
            after_id = root[i].get('wp_after_rev_id')
            for j in range(i,taille_root):
                if(taille_root<=j):
                    print "break"
                    break
                bef_id = root[j].get('wp_before_rev_id')
                aft_id = root[j].get('wp_after_rev_id')
                if(before_id!=bef_id and after_id==bef_id):
                    tmp1=root[i]
                    tmp2 = root[j]
                    compteur +=1
                    print compteur
                    root.remove(tmp1)
                    root.remove(tmp2)
                    taille_root = len(root)
                    break
            
        self.tree.write(nom.encode('utf8'))
        print(str(compteur)+" couple suppr")



                     
    def count_position_error(self,before,after):
        #calcul de la position de l'erreur dans le mot
        i=0
        #print(len(before))
        #print(len(after))
        while(i<len(before) and i <len(after) and before[i]==after[i]):
              i = i+1
        #print i
        return i

    #processing to cvs file
    def treatment_cvs(self,root):
        #print "treatment"
        nom = raw_input("comment voulez vous nommer le fichier de sortie?\nle fichier sera automatiquement suivi de '.csv'\n")
        nom+=".csv"
        fichier_txt = open(nom,"w")#ouverture en ecriture avec ecrasement
        print "file "+nom+" open"
       
        #compteur du nombre de cas traité
        compteur = 0
        nb_cas=0
        #acces aux balises <modif>
        for modif in root:
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
        indice_erreur = self.count_position_error(m_before,m_after)
        fichier_txt.write(str(indice_erreur).encode('utf8')) #indice erreur 
        fichier_txt.write("\t".encode('utf8'))
        fichier_txt.write("1\t".encode('utf8')) #source corpus wicopako = 1
        fichier_txt.write("fr\n".encode('utf8')) #langue

        fichier_txt.close()
        print "file "+nom+" close"
        print "-------"
        
        print("nombre d'element traité ="),
        print(nb_cas)
        
######### Programme ##############
nom =raw_input('nom du fichier à traiter? ')
test = Treatment_xml(nom)
#racine du fichier xml
root = test.get_root()
test.deleting_correction_duplicate(nom,root) #filtre
test.treatment_cvs(root)

