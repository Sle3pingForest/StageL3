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

    def deleting_correction_duplicate(self,nom,root):
        #permet de supprimer les modifications faite puis remise a l'etat initial (fonctionne sur le fichier wikopaco.xml)
        print("deleting_correction_duplicate")
        compteur = 0
        taille_root = len(root)
        #for child in root:
        for i in range(0,taille_root):
            #print taille_root
            #print i
            if(taille_root<=i):
                print "break"
                break
            before_id = root[i].get('wp_before_rev_id')
            after_id = root[i].get('wp_after_rev_id')
            # before_id = child.get('wp_before_rev_id')
            # after_id = child.get('wp_after_rev_id')
            #for modif in root:
            for j in range(i,taille_root):
                if(taille_root<=j):
                    print "break"
                    break
                #print "\tj = ",
                #print str(j)
                #bef_id = modif.get('wp_before_rev_id')
                #aft_id = modif.get('wp_after_rev_id')
                bef_id = root[j].get('wp_before_rev_id')
                aft_id = root[j].get('wp_after_rev_id')
                if(before_id!=bef_id and after_id==bef_id):
                    tmp1=root[i]
                    tmp2 = root[j]
                    compteur +=1
                    print compteur
                    root.remove(tmp1)
                    root.remove(tmp2)
                    #root.remove(child)
                    #root.remove(modif)
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
        # nom ="base_de_cas_WiKoPaCo.csv"
        nom = raw_input("comment voulez vous nommer le fichier de sortie?\nle fichier sera automatiquement suivi de '.csv'\n")
        nom+=".csv"
        fichier_txt = open(nom,"w")#ouverture en ecriture avec ecrasement
        print "file "+nom+" open"
       
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
            indice_erreur = self.count_position_error(m_before,m_after)
            fichier_txt.write(str(indice_erreur).encode('utf8')) #indice erreur mis a 0 pour tester , A MODIFIER!!!
            fichier_txt.write("\t".encode('utf8'))
            fichier_txt.write("1\t".encode('utf8')) #source corpus wicopako = 1
            fichier_txt.write("fr\n".encode('utf8')) #langue

        fichier_txt.close()
        print "file "+nom+" close"
        print "-------"
        
        print("nombre d'element traité ="),
        print(nb_cas)
        
######### Programme ##############
nom = 'wikopaco (copie).xml'
#nom = 'test.xml' #pour tester sur un plus petit fichier

test = Treatment_xml(nom)
#racine du fichier xml
root = test.get_root()
test.deleting_correction_duplicate(nom,root)
test.treatment_cvs(root)

