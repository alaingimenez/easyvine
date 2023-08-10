import pygame
import math



def tour_parcelle(list_gps, pos_actuelle,un_point_gps, zoom,  centre_x,centre_y,cap_actuel):
    """

    transforme la list_gps de coordonnee reelle en coordonnee pygame
    transforme la pos_actuelle  coordonnee reelle en coordonnee pygame
    transforme un_point_gps en un_point_pyg  coordonnee reelle en coordonnee pygame

    :param list_gps: liste a transformer en coordonne pygame
    :param pos_actuelle : a transformer en pos_pygame

    :param screen: ecran
    :param zoom: permet d'agrandir l'image /zoom = 1 pas de zoom/ zoom > 1 = grossi/ zoom < 0 rapetisse / zoom == 0  ERREUR
    :param center: si center = 0 robot a gauche  si center = 1 robot au centre si center = 2 robot a droite
    :param cap_actuel: oriente les coordonnées grace a se cap
    :return: return la liste pour afficher dans pygame
    :return: return l'echelle utilise pour l'affichage l'echelle est calculé grace au tour de la parcelle
    """
    # dans la  list on a des tuples (latitude,longitude)
    # latitude  -> y  / sud nord /
    # longitude -> x  / ouest est /
    # met la position actuelle a gauche / au centre / a droite

    # centre_y = abs((fin_y - deb_y) / 2)

    # recupere les dimension de la fenetre pygame
    deb_x = 0
    fin_y = 0
    fin_x, deb_y = pygame.display.get_window_size()




    # recupere la grandeur utilise par les adresse gps et calcule l'echelle
    la, lo = pos_actuelle  # si la liste gps est vide on initialise avec la pos actuelle
    if len(list_gps) != 0:
        la, lo = list_gps[0]   # si la liste n'a q'un seul element le recuperer
    petite_latitude = la
    grande_latitude = la
    petite_longitude = lo
    grande_longitude = lo
    for i in list_gps:
        la, lo = i
        if la < petite_latitude:
            petite_latitude = la
        elif la > grande_latitude:
            grande_latitude = la
        if lo < petite_longitude:
            petite_longitude = lo
        elif lo > grande_longitude:
            grande_longitude = lo
    lat_gr_pe = grande_latitude - petite_latitude
    long_gr_pe = grande_longitude - petite_longitude
    if lat_gr_pe >= long_gr_pe:
        echelle= lat_gr_pe
    else:
        echelle = long_gr_pe
    if echelle == 0:
        echelle = 1

    #transforme la position actuelle gps en position actuelle pygame
    lat_centre, long_centre = pos_actuelle
    echelle_lat = (deb_y - fin_y) / (echelle)
    lat_pyg_centre = lat_centre - petite_latitude
    lat_pyg_centre = (deb_y - (lat_pyg_centre * echelle_lat * zoom))
    echelle_long = (deb_x - fin_x) / (echelle)
    lon_pyg_centre = long_centre - petite_longitude
    lon_pyg_centre = (deb_x - (lon_pyg_centre * echelle_long * zoom))
    dif_lat_centre =  centre_y - lat_pyg_centre
    dif_long_centre = centre_x - lon_pyg_centre
    lat_pyg_centre = lat_pyg_centre + dif_lat_centre
    lon_pyg_centre = lon_pyg_centre + dif_long_centre

    #transformer les coordonné gps en coordonnée pygame

    list_pyg = []
    for i in list_gps:
        latitude, longitude = i
        echelle_lat = (deb_y - fin_y) / (echelle)
        lat_pyg = (latitude - petite_latitude)  #  petite_latitude
        lat_pyg = (deb_y - (lat_pyg * echelle_lat * zoom))
        lat_pyg = lat_pyg + dif_lat_centre

        echelle_long = (deb_x - fin_x) / echelle
        lon_pyg = longitude - petite_longitude # petite_longitude
        lon_pyg = (deb_x - (lon_pyg * echelle_long * zoom))
        lon_pyg = lon_pyg + dif_long_centre

        # Effectuer la rotation des coordonnées pygame par rapport a cap
        angle = math.radians(-cap_actuel)  # on met -cap pour tourner en sens horaire sinon on tourne en sens anti-horaire
        px = lon_pyg
        py = lat_pyg
        ox = lon_pyg_centre
        oy = lat_pyg_centre
        qx = ox + (px - ox) * math.cos(angle) - (py - oy) * math.sin(angle)
        qy = oy + (px - ox) * math.sin(angle) + (py - oy) * math.cos(angle)
        lon_pyg = qx
        lat_pyg = qy

        list_pyg.append((lon_pyg, lat_pyg)) # ajouter les coordonnées pygame a la liste list_pyg

    position_actuelle_pyg = (lon_pyg_centre, lat_pyg_centre)
    ###################################################
    ## transformer le point

    latitude, longitude = un_point_gps
    echelle_lat = (deb_y - fin_y) / (echelle)
    lat_pyg = (latitude - petite_latitude)  # petite_latitude
    lat_pyg = (deb_y - (lat_pyg * echelle_lat * zoom))
    lat_pyg = lat_pyg + dif_lat_centre

    echelle_long = (deb_x - fin_x) / echelle
    lon_pyg = longitude - petite_longitude  # petite_longitude
    lon_pyg = (deb_x - (lon_pyg * echelle_long * zoom))
    lon_pyg = lon_pyg + dif_long_centre

    # Effectuer la rotation des coordonnées pygame par rapport a cap
    angle = math.radians(-cap_actuel)  # on met -cap pour tourner en sens horaire sinon on tourne en sens anti-horaire
    px = lon_pyg
    py = lat_pyg
    ox = lon_pyg_centre
    oy = lat_pyg_centre
    qx = ox + (px - ox) * math.cos(angle) - (py - oy) * math.sin(angle)
    qy = oy + (px - ox) * math.sin(angle) + (py - oy) * math.cos(angle)
    lon_pyg = qx
    lat_pyg = qy
    un_point_pyg = (lon_pyg,lat_pyg)

    return list_pyg, un_point_pyg, echelle, position_actuelle_pyg  # je retourne la liste mais pas d'interet




def rang_vigne_en_pyg(list_rang_vigne,tour_parcelle_gps, position_actuelle_gps, zoom, centre_x, centre_y, cap_actuel_gps):

    list_rang_pyg = []
    rang_pyg =[]
    index_rang = 0
    for rang in list_rang_vigne: # je recupere les rangs de la vigne
        #print("rang dans rang_vigne_en_pyg " , rang)
        #print (" liste de rang vigne = : " , list_rang_vigne)
        #print(" index de rang = : ", index_rang )
        rang_pyg = []
        for position_complette in rang:
            position_in_rang, occupant_position_in_rang, an_plant, altitude, arroser, travail = position_complette
            lat,long = position_in_rang
            tour_parcelle_pyg, un_point_pyg, echelle, position_actuelle_pyg = tour_parcelle(tour_parcelle_gps,
                                                                                   position_actuelle_gps, (lat,long),
                                                                                   zoom, centre_x, centre_y,
                                                                                   cap_actuel_gps)
            rang_pyg.append((un_point_pyg))
        list_rang_pyg.append(rang_pyg)
        index_rang += 1
    #print("list rang vigne gps = : ", list_rang_vigne)
    #print("list rang py  = : ", list_rang_pyg)
    return list_rang_pyg,tour_parcelle_pyg,position_actuelle_pyg


def evenement_en_pyg(list_evenement,tour_parcelle_gps, position_actuelle_gps, zoom, centre_x, centre_y, cap_actuel_gps):
    tour_parcelle_pyg = []
    evenement_pyg = []
    position_actuelle_pyg = (0,0)
    
    for position in list_evenement: # je recupere les rangs de la vigne

        lat_lon, nom = position
        
        tour_parcelle_pyg, un_point_pyg, echelle, position_actuelle_pyg = tour_parcelle(tour_parcelle_gps,
                                                                                position_actuelle_gps, lat_lon,
                                                                                zoom, centre_x, centre_y,
                                                                                cap_actuel_gps)
        evenement_pyg.append([un_point_pyg, nom])


    return evenement_pyg,tour_parcelle_pyg,position_actuelle_pyg