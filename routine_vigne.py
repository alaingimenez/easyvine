
"""
    dans se fichier il y a les routine qui permette de modifier ou d'afficher la vigne
"""
from routine_gps import *
import pygame

import pickle
import csv


########################################################################
def inverse_sens_range(vigne):# NE SERT PLUS
    """
    inverse le sens de chaque rangé

    :param vigne: liste de coordone gps des rangs composant la vigne chaque rang est decrit par son adresse gps de debut est de fin
                latitude_depart,longitude_depart,latitude_arrive,longitude_arrive = rang
    :return: la liste vigne avec ses coordone depart et arrive de chaque range inverse
    """
    nb_element = len(vigne)
    for i in range(nb_element):
        rang = vigne[i]
        a,b,c,d = rang
        j = c,d,a,b
        vigne.append(j)
    del vigne[:nb_element]
    return(vigne)
#########################################################################



#########################################################################
def create_vigne(name_vigne,origine,largeur_rang,nb_rang,cote):
    """
    permet de creer liste de coordone gps des rangs composant la vigne chaque rang est decrit par son adresse gps de debut est de fin
    latitude_depart,longitude_depart,latitude_arrive,longitude_arrive = rang

    :param origine:      c'est le premier rang :   latitude_depart,longitude_depart,latitude_arrive,longitude_arrive = rang
    :param largeur_rang: en metre c'est la distance entre les rangs
    :param nb_rang :     nombre de rang qui composera la vigne
    :param cote: si = 0 les rangs sont a -90°   si = a 1 les rangs sont a +90°
    :return: la liste de toute les rangs composant la vigne
    """
    lat_depart, long_depart, lat_arrive, long_arrive = origine
    depart = (lat_depart, long_depart)
    arrive = (lat_arrive, long_arrive)
    longueur_rang = distanceGPS(depart, arrive)
    cap_rang = get_angle(depart,arrive )

    #print("")
    #print("variable de routine  create_vigne ")
    #print("longueur du rang : " + str(longueur_rang))
    #print("le cap du rang est en ° : " + str(cap_rang))
    if cote == 0:
        cap_sur_le_cote =  cap_rang - 90
    else:
        cap_sur_le_cote =  cap_rang + 90
        # cap_sur_le_cote = cap_sur_le_cote  % 360
    #print("le cap sur le cote est en ° : " + str(cap_sur_le_cote))

    vigne = []
    vigne.append(origine) # rang 1 de la vigne
    #print("r : 1  " + str(origine))
    if nb_rang > 1:
        for r in range(2,nb_rang + 1): # calcul a partir du rang 2
            #print("r : " + str(r))


            new_depart = new_pointgpt(depart, cap_sur_le_cote, largeur_rang)
            #print("new_depart : ",str(new_depart))


            new_arrive = new_pointgpt(arrive, cap_sur_le_cote , largeur_rang)
            #print("new_arrive : " + str(new_arrive))

            depart = new_depart
            arrive = new_arrive
            lat_depart,long_depart = depart
            lat_arrive,long_arrive = arrive
            rang = (lat_depart, long_depart, lat_arrive, long_arrive)
            vigne.append(rang)

    with open(name_vigne+".vig","wb") as file:
        pickle.dump(vigne,file)
    print("/fin")


    return
#############################################################################################
#############################################################################################
def create_vigne_kml(name_vigne):
    """
    cree le fichier kml a mettre dans maps
    :param name:  nom du fichier
    :param vigne: liste des rangs de la vigne avec leur adresse de depart et de fin
    :return:
    """
    with open(name_vigne + ".vig", "rb") as file:
        vigne = pickle.load(file)

    file = open(name_vigne + "_vigne"+".kml", "w")
    file.write('<?xml version="1.0" encoding="UTF-8"?>' + chr(13))
    file.write('<kml xmlns="http://earth.google.com/kml/2.1">' + chr(13))
    file.write('<Document>' + chr(13) + chr(13))
    for i in vigne:
        file.write('<Placemark>' + chr(13))
        file.write('<name>' + (name_vigne) + '</name>' + chr(13))
        file.write('<Style>' + chr(13))
        file.write('<LineStyle>' + chr(13))
        file.write('<color>ff00ff00</color>' + chr(13))
        file.write('<width>4</width>' + chr(13))
        file.write('</LineStyle>' + chr(13))
        file.write('</Style>' + chr(13))
        file.write('<LineString>' + chr(13))
        file.write('<coordinates>' + chr(13))
        lat_depart,long_depart,lat_arrive,long_arrive = i
        file.write(str(long_depart) + "," + str(lat_depart) + chr(13))
        file.write(str(long_arrive) + "," + str(lat_arrive) + chr(13))
        file.write('</coordinates>' + chr(13))
        file.write('</LineString>' + chr(13))
        file.write('</Placemark>' + chr(13) + chr(13))

    file.write('</Document>' + chr(13))
    file.write('</kml>' )

    file.close()
    return
#############################################################################################
def create_vigne_csv(name_vigne):
    with open(name_vigne + ".vig", "rb") as file:
        vigne = pickle.load(file)
        print (vigne)
        #name_vigne = name_vigne + ".csv"
        #print (name_vigne)
    print("VIGNE")
    print (vigne)
    vigne_convert = []
    for i in vigne:
        a,b,c,d = i
        vigne_convert.append(str(a))
        vigne_convert.append(b)
        vigne_convert.append(c)
        vigne_convert.append(d)

    print("VIGNE_CONVERT")
    print(vigne_convert)

    with open(name_vigne + ".csv", 'w', newline='')as file:
        writer =csv.writer(file) #,delimiter="'",quotechar='|',quoting=csv.QUOTE_MINIMAL)
        for i in vigne_convert:
            writer.writerow([i])




    return

#############################################################################################
def vigne_setend(vigne):
    """
    permet de savoir si la vigne s'éetend a droite ou a gauche du premier rang

    si il n'y a qu'une seul rang return -1

    :param vigne:
    :return: 0 s'étend a gauche     1 s'étend a droite  -1 il n'y a qu'une seule rangé
    """
    rang_1 = vigne[0]
    lat_depart_rang_1, long_depart_rang_1, lat_arrive_rang_1, long_arrive_rang_1 = rang_1
    depart_rang_1 = lat_depart_rang_1, long_depart_rang_1
    arrive_rang_1 = lat_arrive_rang_1, long_arrive_rang_1
    cap_rang = get_angle(depart_rang_1, arrive_rang_1)
    cap_a_droite = cap_rang + 90
    cap_a_gauche = cap_rang - 90
    point_a_droite = new_pointgpt(depart_rang_1, cap_a_droite, 0.20)
    point_a_gauche = new_pointgpt(depart_rang_1, cap_a_gauche, 0.20)

    if len(vigne) == 1: # il n'y a que 1 rang
        cote =  -1

    else: # il y a plusieur rang

        #print ("rang 1 : " + str(rang_1))
        rang_dernier = vigne[len(vigne) - 1]
        #print("rang dernier : " + str(rang_dernier))


        lat_depart_dernier, long_depart_dernier, lat_arrive_dernier, long_arrive_dernier = rang_dernier


        depart_rang_dernier = lat_depart_dernier, long_depart_dernier
        #arrive_rang_dernier = lat_arrive_dernier, long_arrive_dernier


        distance_droite = distanceGPS(point_a_droite,depart_rang_dernier)
        distance_gauche = distanceGPS(point_a_gauche, depart_rang_dernier)

        if distance_droite > distance_gauche:
            cote = 0
        else:
            cote = 1

    return cote
#############################################################################################

def enregistre_parcelle(name,list):
    with open(name + "_p.vig","wb") as file:
        pickle.dump(list,file)

def lecture_parcelle(name):
    with open(name + "_p.vig", "rb") as file:
        list = pickle.load(file)
        return list

def enregistre_rang(name, list):
    with open(name + "_v.vig", "wb") as file:
        pickle.dump(list, file)

def lecture_rang(name):
    with open(name + "_v.vig", "rb") as file:
        return pickle.load(file)


##############################################################################################
##################### routine vigne avec pygame

def next_vigne(list_vigne,indice):
    indice += 1
    if indice > len(list_vigne)-1:
        indice = 0
    name_vigne_en_cours = list_vigne[indice]
    name_vigne_en_cours = format_name_vigne(name_vigne_en_cours, 20)
    return indice,name_vigne_en_cours

def preview_vigne(list_vigne,indice):
    indice += -1
    if indice == -1:
        indice = len(list_vigne) - 1
    name_vigne_en_cours = list_vigne[indice]
    name_vigne_en_cours = format_name_vigne(name_vigne_en_cours, 20)
    return indice,name_vigne_en_cours

def format_name_vigne(name,nb_caractere):
    if len(name) < nb_caractere:  # formater le nom de la vigne a nb_caractere
        for i in range(len(name), nb_caractere):
            name = name + " "
    return name

def add_debut_rang_in_list_rang(position_complette_in_rang, list_rang_vigne,largeur_vigne ):

    # ajouter la position_complette_in_rang au debut d'un nouveau rang
    rang = [position_complette_in_rang] # ICI Il faut essayer de mettre 2 crochet de plus
    list_rang_vigne.append(rang)
    #list_rang_vigne[x].append(position_complette_in_rang)

    # recuperer la largeur_vigne c'est la largeur entre les rangs
    #largeur_vigne
    pourcentage_largeur_vigne = largeur_vigne - (largeur_vigne * 15/100)

    # recupere la lat et la long de la position a ajouter (position_complette_in_rang) et les mettre dans new_position
    position_in_rang, occupant_position_in_rang, an_plant, altitude, arroser, travail = position_complette_in_rang
    lat, long = position_in_rang
    new_position = (lat, long)

    list_dist_cap =[] # creer un liste pour mettre la distance du premier rang au autre rang

    # chercher le cap de l'etalement de la vigne de rang a rang /TESTER LE CAP D'UNE ADRESSE DEPART RANG A L'adresse du depart rang d a coté
    if len(list_rang_vigne) > 0:  # verifier le cap d'une rangé a l'autre
        for x in range(0,len(list_rang_vigne) -1 ): # -1
            position_c = list_rang_vigne[0][0] # position_c = list_rang_vigne[x][0]
            position_in_rang, occupant_position_in_rang, an_plant, altitude, arroser, travail = position_c
            lat, long = position_in_rang
            position_debut = (lat, long) # recupere la position du debut premier rang pour creer la list_dist_cap

            position_c = list_rang_vigne[x + 1][0]
            position_in_rang, occupant_position_in_rang, an_plant, altitude, arroser, travail = position_c
            lat, long = position_in_rang
            position_suivante = (lat, long) # recupere la position du rang suivante  pour creer la list_dist_cap

            position_c = list_rang_vigne[x ][0]
            position_in_rang, occupant_position_in_rang, an_plant, altitude, arroser, travail = position_c
            lat, long= position_in_rang
            position_liste = (lat, long) # recuperer les positions de la liste pour les comparer a new position

            # si la nouvelle position ne correspond pas a un depart de ranger la retirer
            if get_distance_gps(new_position, position_liste) < pourcentage_largeur_vigne :
                del(list_rang_vigne[-1]) # on retire la nouvelle position que l(on avait ajouté en fin de liste car elle n'est pas coherante( trops pres d'un debute de rang)
                return False, list_rang_vigne

            # ajouter la longueur des segment et leur cap a la liste
            list_dist_cap.append((get_distance_gps(position_debut, position_suivante), get_angle(position_debut, position_suivante)))

            # comparer les longueur de segment pour trier les debut de rang
            for dc in range(0,len(list_dist_cap)-1):
                distA, capA = list_dist_cap[dc]
                distB, capB = list_dist_cap[dc + 1]
                if distA > distB:
                    print ("il faut inverser l'adresse : ",dc + 2,"avec ladresse  : ",dc + 1)
                    rang_a_mettre_avant = list_rang_vigne[dc + 2]
                    del(list_rang_vigne[dc + 2])
                    list_rang_vigne.insert(dc +1 ,rang_a_mettre_avant )

    return True,list_rang_vigne

def add_fin_rang_in_list_rang(position_complette_in_rang, list_rang_vigne,largeur_vigne  ):
    # recuperer la largeur_vigne
    #largeur_vigne, distance_souche, cepage = info_vigne_encours
    pourcentage_largeur_vigne = largeur_vigne - (largeur_vigne * 15/100)
    new_position_fin_in_rang = (0, 0)

    for x in range(len(list_rang_vigne)-1,-1,-1):
        if len(list_rang_vigne[x]) == 2:  # il y a une adresse de fin de rang donc controler si la nouvelle adresse n'est pas trop proche
            new_position_fin_in_rang, occupant_position_in_rang, an, altitude, a_arroser, travaux = position_complette_in_rang
            lat, long = new_position_fin_in_rang
            new_position_fin = (lat, long)
            position_existante, occupant_position_in_rang, an, altitude, a_arroser, travaux = list_rang_vigne[x][1]
            lat, long = position_existante
            position_existante_fin = (lat, long)
            if get_distance_gps(new_position_fin, position_existante_fin) < pourcentage_largeur_vigne:
                return False, list_rang_vigne



    # regarder si il reste des debut de rang sans fin de rang et des meme adresse de fin de rang
    tous_les_rang_sont_ok = True
    for rang in list_rang_vigne:
        if len(rang) == 1:
            tous_les_rang_sont_ok = False
            break
    if tous_les_rang_sont_ok:
        print("TOUS LES RANGS SONT COMPLET IMPOSSIBLE D'AJOUTER CETTE ADRESSE")
        return False, list_rang_vigne
    # rechercher a partir de la fin dans la list_rang_vigne les rang qui ont deja une adresse de debut rang si il n'on pas la fin de rang l'ajouter
    for x in range(len(list_rang_vigne)-1,-1,-1): # longueur de la liste -1 jusqu'a -1 avec un step de -1
        rang = list_rang_vigne[x]
        if len(rang) == 1:
            list_rang_vigne[x].append(position_complette_in_rang)
            index_new_rang = x
            break

    # controler que l'adresse qu l'on est en train d'ajouter ne soit pas a moins de de la largeur de rang



    # controler si la rangé que je vien d'ajouter croise une autre rangé
    # recupere la lat et la long de la position a ajouter (position_complette_in_rang) et les mettre dans new_position
    #self.parcel.position = (self.position_gps, "AMMARE", "2023", self.altitude_gps, self.a_arroser, self.list_travaux_piquet[self.index_travaux_piquet])
    position_in_rang, occupant_position_in_rang, an, altitude, a_arroser, travaux = list_rang_vigne[index_new_rang][0]
    lat, long = position_in_rang
    new_position_debut = (lat, long)
    position_in_rang, occupant_position_in_rang, an, altitude, a_arroser, travaux = list_rang_vigne[index_new_rang][1]
    lat, long = new_position_fin_in_rang
    new_position_fin = (lat, long)

    # ci dessou cree la liste des rangé qui se croise si le scanneur ne fait pas attention quand il scanne les fin de rang
    list_x =[]
    for x in range(len(list_rang_vigne)-1,-1,-1): # longueur de la liste -1 jusqu'a element 0 inclus avec un step de -1
        if x != index_new_rang:
            rang = list_rang_vigne[x]
            if len(rang) == 2:
                position_in_rang, occupant_position_in_rang, an, altitude, a_arroser, travaux = list_rang_vigne[x][0]
                lat, long  = position_in_rang
                position_x_debut = (lat, long)
                position_in_rang, occupant_position_in_rang, an, altitude, a_arroser, travaux = list_rang_vigne[x][1]
                lat, long  = position_in_rang
                position_x_fin = (lat, long)
                if check_segments_intersection(new_position_debut, new_position_fin, position_x_debut, position_x_fin):
                    #print ("la nouvelle rangé index : ",index_new_rang,"    croise la rangé x : ", x)
                    list_x.append(x)
    list_x.append(index_new_rang)

    #ci dessou on se sert de la liste des range qui se croise pour decroiser les rangés
    for x in range(len(list_x)-1,0,-1): # permet de decroiser les rangers si on se trompe en scannan
        sav_position_in_rang, occupant_position_in_rang, an, altitude, a_arroser, travaux = list_rang_vigne[list_x [x - 1]][1]
        list_rang_vigne[list_x[x-1]][1] = [new_position_fin_in_rang, occupant_position_in_rang, an, altitude, a_arroser, travaux ]
        list_rang_vigne[list_x[x]][1] = [sav_position_in_rang, occupant_position_in_rang, an, altitude, a_arroser, travaux ]
    return True, list_rang_vigne

def undo_in_list_rang_vigne(position, list_rang_vigne):
    print("position ", position)
    for rang in list_rang_vigne:
        print(rang)
        if position in rang:
            print ("j'ai trouver l'element")
            rang.remove(position)
            if len(rang) == 0:
                list_rang_vigne.remove(rang)

def position_rang_in_list(list_rang_vigne, rang,pos):
    """
    pos = 0 pour adresse de debut de rang 
    pos = -1 pour adresse fin de rang
    """
    position_in_rang, occupant_position_in_rang, etat_occupant_in_rang, action_sur_occupant = list_rang_vigne[rang][pos]
    lat, long, haut = position_in_rang
    return (lat, long)