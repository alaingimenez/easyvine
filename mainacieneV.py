# This is a sample Python script.

# rajouter a info vigne le nombre de rangé

import os
import math
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
button = 4  #  c'est le bouton qui est sur le manche a droite et qui permet de scanner les rangs
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
button_state = GPIO.HIGH

from communication import *
from routine_robot import *
import routine_gps
import pyg


from gps import *
import threading

import pygame
pygame.init()


gpsd = None # seting the global variable
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


gpsp = GpsPoller() # create the thread
gpsp.start() # start it up





def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':







 

    BLACK = (0, 0, 0)
    GRAY = (127, 127, 127)
    WHITE = (255, 255, 255)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    # le gps qui dirige est sur l'essieux  avant mais il peut etre au centre ou decale sur le centre de la roue gauche ou droite
    # ou  0 = a gauche    1 = au centre   2 = a droite  dans mon cas il est a gauche donc = a 0

    # l'outil est entre les roues avant et arriere il peut etre au centre a droite ou a gauche
    #  0 = a gauche    1 = au centre   2 = a droite  dans mon cas il est a droite  donc = a 2
    # il faut connaitre
    # 1er  la distance en largeur du bout de l'outil au GPS en metre                d_outil_gps
    # 2em  la largeur de travail de l'outil en metre                                l_travail
    # 3em le decalage entre le bout de l'outil et le centre du rang  en metre       d_outil_rang

    # PARAMETRE ROBOT
    empattement_robot = 0.8# metre
    voie_robot = 0.60# metre
    d_outil_gps = 0.6
    l_travail = 0.10
    d_outil_rang = .05
    robot = (empattement_robot,voie_robot,d_outil_gps,d_outil_rang  )

    position_robot = (43.184419, 2.791868)

    # CREATION DE LA VIGNE
    name_vigne = "vigne_longue"  # nom du fichier sur le disque
    rang_1 = (43.184465, 2.792083, 43.184949, 2.792167) # adresse de depart et d'arrive du premier rang
    largeur_rang = 2
    nb_rang = 10
    cote = 0 # 0 la vigne s'etend vers la gauche  1 la vigne s'etend  vers la droite

    create_vigne(name_vigne,rang_1, largeur_rang, nb_rang, cote)
    create_vigne_kml(name_vigne) # CREATION DU FICHIER KML original
    create_vigne_csv(name_vigne)


    parcours_robot = create_parcours_robot(robot, position_robot, name_vigne)
    create_parcours_robot_kml(name_vigne, parcours_robot)
    create_parcour_csv(name_vigne, parcours_robot)


#############  A PARTIR D'ICI LE PROGRAMME POUR SCANNER ET TRAVAILLER LA VIGNE

    #definir le screen
    width = 1000
    heigh = 1000
    deb_x = 0
    fin_y = 0
    fin_x, deb_y = width, heigh
    screen = pygame.display.set_mode((width,heigh))

    #charger la liste des vignes _v et _p  pour vigne et parcelle // on se retrouve avec 2 fichier par vigne
    chemin_disk = "vigne/"
    list_vigne = os.listdir(chemin_disk)
    list_vigne.sort()
    # enleve les fins _v.vig   ou _p.vig  // on se retrouve avec une liste ou il y a 2 fois le meme nom pour la vigne
    #print (list_vigne)
    l = []
    for i in list_vigne:
        i =(i[:-6]) #garde seulement le nom de la vigne
        l.append(i)
    # ici nous avons une liste avec 2 nom pour la meme vigne 1 pour la parcelle _p.vig et 1 pour les rang _v.vig
    #print(l)
    list_vigne = []
    for i in l:
        if i not in list_vigne: # permet de se retrouver avec une liste de 1 nom par vigne
            list_vigne.append(i)
    
    #print(list_vigne)
    indice_vigne_en_cours = 0 # c'est l'indice dans la list_vigne

    list_rang_vigne = [] # c'est dans cette variable que nous avons tous les rang de la vigne
    list_rang_vigne_pyg = [] # dans cette variable noous avons juste les coordonnée des souche dans les rang en pyg
    info_vigne_encours = [2,1.1,"carignan"]
    flag_info_vigne = False  # si = a True c'est que l'on est dans le menu info vigne encours
    creat_quel_info = 0  # 0 c'est que l'on rentre le nom de la vigne 1 la largeur du rang  2 la distance souche 3 le cepage
    creat_name_vigne = "" # c'est la que l'on va mettre le nom de la vigne pendant qu'on la crée
    creat_largeur_rang = ""
    creat_distance_souche = ""
    creat_cepage = ""

    list_outil = ["Scan","Fichier", "Simulation", "DK", "ROBOT","Create"] #creer la liste outil et la formate a 10 carcatere
    l_o =[]
    for outil in list_outil:
        if len(outil) < 10:
            for nbs in range(len(outil), 10):
                outil = outil + " "
        l_o.append(outil)
    list_outil = l_o
    indice_outil_en_cours = 0

    list_scan_quoi = [" PARCELLE ", "   RANG   "," EVENEMENT"] #, " POSITION ", "  INCIDENT ", "  ACTION  "]
    indice_scan_quoi_en_cours = 0
    scan_mode_scan = 0 #  0 = VIEW   1 = PAUSE 2 = REC
    scan_distance_point = 1  # c'est la distance entre les point quand on scanne le tour de la parcelle
    tour_parcelle_pyg = []   # c'est la liste des points de la parcelle pour affichage pygame
    echelle = []             # c'est l'echelle entre les 2 point les plus eloigné pur affichage pygame
    position_actuelle_pyg = [] # c'est la position actuelle pour affichage pygame
    tour_parcelle_gps = []     # c'est la liste des points gps du tour de la parcelle
    tour_parcelle_gps_undo = [] # quan on clique sur undo la derniere adresse de la liste tour_parcelle_gps va dans la liste tour_parcelle_gps_undo
    position_rang_undo = [] # quand on ajoute un debut de rang ou une fin de rang la position vas dans cette liste
    position_rang_redo = [] # quand on click sur undo la derniere position de undo va dans redo  et elle est effacé de la list_rang_vigne
    parcelle_tour_et_info = [info_vigne_encours , tour_parcelle_gps]

    list_evenement = [" AUCUN ", "REMPLACER", " ARROSER ", " MONTER ", " RABATTRE "]
    indice_list_evenement = 0


    list_scan_rang = ["DEBUT RANG", " FIN RANG ", " SOUCHE ", " PIQUET "]
    indice_scan_rang_en_cours  = 0

    position_actuelle_gps = (0,0)
    cap_actuel_gps = 0
    zoom = 1      # permet de zoomer dans l'ecran pygame
    centre_x = 400   # centre la position actuelle dans l'ecran pygame
    centre_y = 400  # centre la position actuelle dans l'ecran pygame



    ##################################################################################################
    # Affichage
    font = pygame.font.Font('freesansbold.ttf', 30)  # chargement de la fonte a utiliser
    font_alerte = pygame.font.Font('freesansbold.ttf', 60)

    alerte_save = font_alerte.render(str("| SAVING |"), True, GREEN, WHITE)
    alerte_saveRect = alerte_save.get_rect()
    alerte_saveRect.x = 10
    alerte_saveRect.y = 300
    time_alerte_save = 1.5

    # creer le bouton select vignes avec le nom de la vigne est les 2 boutton pour changer de vigne
    bouton_vigne_en_cours_g = font.render(str("<< :" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_chang_vigne_gRect = bouton_vigne_en_cours_g.get_rect()
    xb, yb, wb, hb = bouton_vigne_en_cours_g.get_rect()
    bouton_chang_vigne_gRect.x = 10  # position le texte en width
    bouton_chang_vigne_gRect.y = heigh - 10 - hb # position le texe en heigh en se servant de sa hauteur

    name_vigne_en_cours  = list_vigne[indice_vigne_en_cours] # chargement de la vigne en cours
    name_vigne_en_cours = format_name_vigne(name_vigne_en_cours, 20)
    parcelle_tour_et_info = lecture_parcelle(chemin_disk + list_vigne[indice_vigne_en_cours])
    info_vigne_encours,tour_parcelle_gps = parcelle_tour_et_info
    #print(info_vigne_encours)
    #print(tour_parcelle_gps)
    list_rang_vigne = lecture_rang(chemin_disk + list_vigne[indice_vigne_en_cours])
    text_vigne_en_cours = font.render(str(name_vigne_en_cours), True, GREEN, BLUE)  # transformer le texte en graphique
    text_vigne_en_coursRect = text_vigne_en_cours.get_rect() # recuperer le rectangle du texte
    xv,yv,wv,hv = text_vigne_en_cours.get_rect()  # recuperer la position la largeur et hauteur du texte
    text_vigne_en_coursRect.x = 10 + wb + 5   # position le texte 10 + largeur  bouton gauche  + 5 en width
    text_vigne_en_coursRect.y = heigh - 10 - hb # position le texe en heigh en se servant de sa hauteur

    bouton_vigne_en_cours_d = font.render(str(": >>" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_chang_vigne_dRect = bouton_vigne_en_cours_d.get_rect()
    bouton_chang_vigne_dRect.x = 10 + wb + wv + 10   # 10 + largeur bouton gauche + largeur texte texte en width
    bouton_chang_vigne_dRect.y = heigh - 10 - hb # position le texe en heigh en se servant de sa hauteur

    libelle_vigne_encours = font.render("Vigne encours", True, WHITE, BLACK)
    libelle_vigne_encoursRect = libelle_vigne_encours.get_rect()
    libelle_vigne_encoursRect.x = 10 + wb + 5
    libelle_vigne_encoursRect.y = heigh - 10 - (hb * 2)

    bouton_info_vigne_en_cours = font.render(str("| INFO |" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_info_vigne_en_coursRect = bouton_info_vigne_en_cours.get_rect()
    bouton_info_vigne_en_coursRect.x = 120   # 10 + largeur bouton gauche + largeur texte texte en width
    bouton_info_vigne_en_coursRect.y = heigh - 10 - (hb * 3) # position le texe en heigh en se servant de sa hauteur

    libelle_largeur_rang = font.render("largeur rang  : " + format(info_vigne_encours[0], '.2f') +str("M") , True, WHITE, BLACK)
    libelle_largeur_rangRect = libelle_largeur_rang.get_rect() #font.render(format(zoom, '.2f')
    libelle_largeur_rangRect.x = 10
    libelle_largeur_rangRect.y = 400

    libelle_distance_cep = font.render("distance cep  : "+ format(info_vigne_encours[1], '.2f')+"M", True, WHITE, BLACK)
    libelle_distance_cepRect = libelle_distance_cep.get_rect()
    libelle_distance_cepRect.x = 10
    libelle_distance_cepRect.y = 440

    libelle_cepage = font.render("cepage  : "+ str(info_vigne_encours[2]) , True, WHITE, BLACK)
    libelle_cepageRect = libelle_cepage.get_rect()
    libelle_cepageRect.x = 10
    libelle_cepageRect.y = 480

    libelle_nb_range = font.render("NB Rangé : " + str(len(list_rang_vigne)), True, WHITE, BLACK)
    libelle_nb_rangeRect = libelle_nb_range.get_rect()
    libelle_nb_rangeRect.x = 10
    libelle_nb_rangeRect.y = 520

    ## -------
    ## creer les bouton zoom
    libelle_zoom = font.render("ZOOM", True, WHITE, BLACK)
    libelle_zoomRect = libelle_zoom.get_rect()
    libelle_zoomRect.x = 400
    libelle_zoomRect.y = heigh - 10 - (hb * 2)

    bouton_zoom_g = font.render(str("<< :" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_zoom_gRect = bouton_zoom_g.get_rect()
    # xb, yb, wb, hb = bouton_vigne_en_cours_g.get_rect()
    bouton_zoom_gRect.x = 355 # position le texte en width
    bouton_zoom_gRect.y = heigh - 10 - hb # position le texe en heigh en se servant de sa hauteur


    text_zoom = font.render(format(zoom, '.2f'),True,GREEN, BLUE)
    text_zoomRect = text_zoom.get_rect()
    text_zoomRect.x = 411
    text_zoomRect.y = heigh - 10 - hb

    bouton_zoom_d = font.render(str(": >>" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_zoom_dRect = bouton_zoom_d.get_rect()
    # xb, yb, wb, hb = bouton_vigne_en_cours_g.get_rect()
    bouton_zoom_dRect.x = 473 # position le texte en width
    bouton_zoom_dRect.y = heigh - 10 - hb # position le texe en heigh en se servant de sa hauteur

    # ---- creer les boutons de centrage
    bouton_centre_h = font.render(str("^^" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_centre_hRect = bouton_centre_h.get_rect()
    # xb, yb, wb, hb = bouton_vigne_en_cours_g.get_rect()
    bouton_centre_hRect.x = 30 # position le texte en width
    bouton_centre_hRect.y = heigh - 145 # position le texe en heigh en se servant de sa hauteur

    bouton_centre_d = font.render(str(">>" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_centre_dRect = bouton_centre_d.get_rect()
    # xb, yb, wb, hb = bouton_vigne_en_cours_g.get_rect()
    bouton_centre_dRect.x = 50 # position le texte en width
    bouton_centre_dRect.y = heigh - 110 # position le texe en heigh en se servant de sa hauteur

    bouton_centre_b = font.render(str("vv" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_centre_bRect = bouton_centre_b.get_rect()
    # xb, yb, wb, hb = bouton_vigne_en_cours_g.get_rect()
    bouton_centre_bRect.x = 30 # position le texte en width
    bouton_centre_bRect.y = heigh - 75 # position le texe en heigh en se servant de sa hauteur

    bouton_centre_g = font.render(str("<<" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_centre_gRect = bouton_centre_g.get_rect()
    # xb, yb, wb, hb = bouton_vigne_en_cours_g.get_rect()
    bouton_centre_gRect.x = 10 # position le texte en width
    bouton_centre_gRect.y = heigh - 110 # position le texe en heigh en se servant de sa hauteur

    ## ---- a partir afficher le menu outil
    # creer le bouton select outil avec le nom de l'outil est les 2 boutton pour changer d'outil
    bouton_outil_en_cours_g = font.render(str("<< :" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_chang_outil_gRect = bouton_outil_en_cours_g.get_rect()
    wa = 50
    bouton_chang_outil_gRect.x = 504 + wa# position le texte en width
    bouton_chang_outil_gRect.y = heigh - 10 - hb # position le texe en heigh en se servant de sa hauteur

    name_outil_en_cours  = list_outil[indice_outil_en_cours] # chargement de l'outil en cours
    text_outil_en_cours = font.render(str(name_outil_en_cours), True, GREEN, BLUE)  # transformer le texte en graphique
    text_outil_en_coursRect = text_outil_en_cours.get_rect() # recuperer le rectangle du texte
    text_outil_en_coursRect.x = 560  + wa  # position le texte 10 + largeur  bouton gauche  + 5 en width
    text_outil_en_coursRect.y = heigh - 10 - hb  # position le texe en heigh en se servant de sa hauteur

    bouton_outil_en_cours_d = font.render(str(": >>" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_chang_outil_dRect = bouton_outil_en_cours_d.get_rect()
    bouton_chang_outil_dRect.x = 685 + wa# 10 + largeur bouton gauche + largeur texte texte en width
    bouton_chang_outil_dRect.y = heigh - 10 - hb  # position le texe en heigh en se servant de sa hauteur

    libelle_outil_encours = font.render("Outil encours", True, WHITE, BLACK)
    libelle_outil_encoursRect = libelle_outil_encours.get_rect()
    libelle_outil_encoursRect.x = 580
    libelle_outil_encoursRect.y = heigh - 10 - (hb * 2)
    ## -------

    #############  Creer menu outil SCAN

    bouton_scan_quoi_g = font.render(str("<< :" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_scan_quoi_gRect = bouton_scan_quoi_g.get_rect()
    bouton_scan_quoi_gRect.x = 10  # position le texte en width
    bouton_scan_quoi_gRect.y = 10 # position le texe en heigh en se servant de sa hauteur

    name_scan_quoi_en_cours  = list_scan_quoi[indice_scan_quoi_en_cours] # chargement de la liste /PARCELLE/ /RANG/
    text_scan_quoi_en_cours = font.render(str(name_scan_quoi_en_cours), True, GREEN, BLUE)  # transformer le texte en graphique
    text_scan_quoi_en_coursRect = text_scan_quoi_en_cours.get_rect() # recuperer le rectangle du texte
    text_scan_quoi_en_coursRect.x = 65  # position le texte 10 + largeur  bouton gauche  + 5 en width
    text_scan_quoi_en_coursRect.y = 10# position le texe en heigh en se servant de sa hauteur

    bouton_scan_quoi_d = font.render(str(": >>" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_scan_quoi_dRect = bouton_scan_quoi_d.get_rect()
    bouton_scan_quoi_dRect.x = 243 # position le texte en width
    bouton_scan_quoi_dRect.y = 10 # position le texe en heigh en se servant de sa hauteur
    ## -- ci dessou les bouton pour scanner le tour de la parcelle
    bouton_rec = font.render("|  REC  |", True, YELLOW, GRAY)
    bouton_recRect = bouton_rec.get_rect()
    bouton_recRect.x = 320
    bouton_recRect.y = 10

    bouton_pause = font.render("|PAUSE|", True, YELLOW, GRAY)
    bouton_pauseRect = bouton_pause.get_rect()
    bouton_pauseRect.x = 320 +120
    bouton_pauseRect.y = 10

    bouton_undo = font.render("|UNDO |", True, YELLOW, GRAY)
    bouton_undoRect = bouton_undo.get_rect()
    bouton_undoRect.x = 320
    bouton_undoRect.y = 50

    bouton_redo = font.render("| REDO |", True, YELLOW, GRAY)
    bouton_redoRect = bouton_redo.get_rect()
    bouton_redoRect.x = 320 + 120
    bouton_redoRect.y = 50

    bouton_view = font.render("| VIEW |", True, YELLOW, GRAY)
    bouton_viewRect = bouton_view.get_rect()
    bouton_viewRect.x = 680
    bouton_viewRect.y = 10

    bouton_delete = font.render("|DELET|", True, YELLOW, GRAY)
    bouton_deleteRect = bouton_delete.get_rect()
    bouton_deleteRect.x = 680
    bouton_deleteRect.y = 50

    bouton_save = font.render("| SAVE |", True, YELLOW, GRAY)
    bouton_saveRect = bouton_save.get_rect()
    bouton_saveRect.x = 680
    bouton_saveRect.y = 90

    libelle_distance_point = font.render("Distance Points", True, WHITE, BLACK)
    libelle_distance_pointRect = libelle_distance_point.get_rect()
    libelle_distance_pointRect.x = 10 + 20
    libelle_distance_pointRect.y = 50

    bouton_distance_point_g = font.render(str("<< :" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_distance_point_gRect = bouton_distance_point_g.get_rect()
    bouton_distance_point_gRect.x = 10 + 30 # position le texte en width
    bouton_distance_point_gRect.y = 80 # position le texe en heigh en se servant de sa hauteur

    text_scan_distance_point = font.render(str(scan_distance_point), True, GREEN, BLUE)  # transformer le texte en graphique
    text_scan_distance_pointRect = text_scan_distance_point.get_rect() # recuperer le rectangle du texte
    text_scan_distance_pointRect.x = 67 + 30 # position le texte 10 + largeur  bouton gauche  + 5 en width
    text_scan_distance_pointRect.y = 80# position le texe en heigh en se servant de sa hauteur

    bouton_distance_point_d = font.render(str(": >>" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_distance_point_dRect = bouton_distance_point_d.get_rect()
    bouton_distance_point_dRect.x = 130 + 30 # position le texte en width
    bouton_distance_point_dRect.y = 80 # position le texe en heigh en se servant de sa hauteur

    ## -- CI DESSOU LES BOUTON POUR SCANNER LES RANGS
    bouton_select_deb_fin_rang_g = font.render(str("<< :" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_select_deb_fin_rang_gRect = bouton_select_deb_fin_rang_g.get_rect()
    bouton_select_deb_fin_rang_gRect.x = 10
    bouton_select_deb_fin_rang_gRect.y = 60

    bouton_select_deb_fin_rang_d = font.render(str(": >>" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_select_deb_fin_rang_dRect = bouton_select_deb_fin_rang_d.get_rect()
    bouton_select_deb_fin_rang_dRect.x = 285
    bouton_select_deb_fin_rang_dRect.y = 60



    rang_bouton_debut_rang = font.render(str(list_scan_rang[indice_scan_rang_en_cours]), True, GREEN, BLUE)
    rang_bouton_debut_rangRect = rang_bouton_debut_rang.get_rect()
    rang_bouton_debut_rangRect.x = 65
    rang_bouton_debut_rangRect.y = 60

    rang_bouton_enregistre_position = font.render("| CLICK FOR SCAN |", True, YELLOW, GRAY)
    rang_bouton_enregistre_positionRect = rang_bouton_enregistre_position.get_rect()
    rang_bouton_enregistre_positionRect.x = 360
    rang_bouton_enregistre_positionRect.y = 60

    rang_bouton_undo = font.render("|UNDO |", True, YELLOW, GRAY)
    rang_bouton_undoRect = rang_bouton_undo.get_rect()
    rang_bouton_undoRect.x = 360
    rang_bouton_undoRect.y = 10

    rang_bouton_redo = font.render("| REDO |", True, YELLOW, GRAY)
    rang_bouton_redoRect = rang_bouton_redo.get_rect()
    rang_bouton_redoRect.x = 360 + 130
    rang_bouton_redoRect.y = 10

    ################### CI DESSOU LES BOUTON POUR SCANNER LES EVENEMENTS
    bouton_evenement_g = font.render(str("<< :" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_evenement_gRect = bouton_evenement_g.get_rect()
    bouton_evenement_gRect.x = 10 + 250 # position le texte en width
    bouton_evenement_gRect.y = 100 # position le texe en heigh en se servant de sa hauteur

    name_evenement_en_cours  = list_evenement[indice_list_evenement] # 
    text_evenement_en_cours = font.render(str(name_evenement_en_cours), True, GREEN, BLUE)  # transformer le texte en graphique
    text_evenement_en_coursRect = text_evenement_en_cours.get_rect() # recuperer le rectangle du texte
    text_evenement_en_coursRect.x = 80 + 250  # position le texte 10 + largeur  bouton gauche  + 5 en width
    text_evenement_en_coursRect.y = 100# position le texe en heigh en se servant de sa hauteur

    bouton_evenement_d = font.render(str(": >>" ), True, YELLOW, GRAY)  # transformer le texte en graphique
    bouton_evenement_dRect = bouton_scan_quoi_d.get_rect()
    bouton_evenement_dRect.x = 270 + 250  # position le texte en width
    bouton_evenement_dRect.y = 100 # position le texe en heigh en se servant de sa hauteur

    text_libelle_evenement = font.render("EVENEMENT -> ", True, WHITE, BLACK)
    text_libelle_evenementRect = text_libelle_evenement.get_rect()
    text_libelle_evenementRect.x = 10 
    text_libelle_evenementRect.y = 100




    ##  outil CREAT
    fichier_libelle_nom_vigne = font.render("Nom  Vigne : ", True, WHITE, BLACK)
    fichier_libelle_nom_vigneRect = fichier_libelle_nom_vigne.get_rect()
    fichier_libelle_nom_vigneRect.x = 10
    fichier_libelle_nom_vigneRect.y = 50

    fichier_libelle_largeur_rang = font.render("Largeur rang : ", True, WHITE, BLACK)
    fichier_libelle_largeur_rangRect = fichier_libelle_largeur_rang.get_rect()
    fichier_libelle_largeur_rangRect.x = 10
    fichier_libelle_largeur_rangRect.y = 90

    fichier_libelle_distance_souche = font.render("Distance souche : ", True, WHITE, BLACK)
    fichier_libelle_distance_soucheRect = fichier_libelle_distance_souche.get_rect()
    fichier_libelle_distance_soucheRect.x = 10
    fichier_libelle_distance_soucheRect.y = 130

    fichier_libelle_cepage = font.render("   Cepage : ", True, WHITE, BLACK)
    fichier_libelle_cepageRect = fichier_libelle_cepage.get_rect()
    fichier_libelle_cepageRect.x = 10
    fichier_libelle_cepageRect.y = 170

    bouton_vigne = font.render("|                    |", True, YELLOW,GRAY)
    bouton_vigneRect = bouton_vigne.get_rect()
    bouton_vigneRect.x = 280
    bouton_vigneRect.y = 50

    bouton_largeur_rang = font.render("| 0.00 |", True, YELLOW, GRAY)
    bouton_largeur_rangRect = bouton_largeur_rang.get_rect()
    bouton_largeur_rangRect.x = 280
    bouton_largeur_rangRect.y = 90

    bouton_distance_souche = font.render("| 0.00 |", True, YELLOW, GRAY)
    bouton_distance_soucheRect = bouton_largeur_rang.get_rect()
    bouton_distance_soucheRect.x = 280
    bouton_distance_soucheRect.y = 130

    bouton_cepage = font.render("|                    |", True, YELLOW, GRAY)
    bouton_cepageRect = bouton_cepage.get_rect()
    bouton_cepageRect.x = 280
    bouton_cepageRect.y = 170

    ################################################################################################

    # pour effectuer un essai de scan tour parcelle la position actuelle est mise dans le tour de parcelle
    position_actuelle=[(43.186083, 2.790960)
                       ,(43.187753, 2.790569)
                       ,(43.187788, 2.790862)
                       ,(43.186127, 2.791254)
                       ,(43.186121, 2.791161)
                       ,(43.186109, 2.791037)
]
    cap_actuel= [0,90,180,270,270,270
  ]
    lng_essai = len(position_actuelle)
    i_essai = 0

    list_debut_rang = [(43.186108, 2.790951, 1)
                       ,(43.186114, 2.790975,1)
        , (43.186125, 2.791052, 1)
                       ,(43.186117, 2.791000,1)
                       ,(43.186122, 2.791026,1)
                       ,(43.186125, 2.791052, 1)
                       , (43.186129, 2.791077, 1)]

    list_fin_rang = [
         (43.186419, 2.790878, 1)
        ,(43.186437, 2.791003, 1)
        , (43.186437, 2.790952, 1)
        , (43.186422, 2.790905, 1)
        , (43.186437, 2.790952, 1)
         ,(43.186437, 2.790981, 1)

        , (43.186433, 2.790927, 1)
        , (43.186437, 2.790952, 1)











    ]
    index_debut_rang = 0
    index_fin_rang = 0

    #################################
    ########### essai pour la liste rangé
    #######################################
    latitude, longitude,hauteur = 43.185418, 2.791491, 1
    position_in_rang = (latitude, longitude,hauteur)
    occupant_position_in_rang = "souche" # piquet /amare
    etat_occupant_in_rang = "ok" # hs ou manque
    action_sur_occupant = ["arroser","rien"] # arroser angrais monter rabaisser

    position_complette_in_rang = [position_in_rang,occupant_position_in_rang,etat_occupant_in_rang,action_sur_occupant]

    rang = [position_complette_in_rang ,position_complette_in_rang ]
    #print(rang)
    vigne = [rang,rang]
    print("vigne  :", vigne)
    for rang in vigne:
        pass
        #print("la vigne est compose de : ", rang)
        for i in rang:
            pass
            #print ("le rang est compose  : ", i)

    erreurio = 0
    pitch = -1
    run = True
    while run:  # DEBUT DE BOUCLE PRINCIPALE
        try:
            holdcompas = 0
            compascmps = read_compas_cmps(holdcompas)
            pitch = read_pitch()
            roll = read_roll()
            #print("compas cmps : " ,compascmps, "   pitch : ", pitch, "   roll : ", roll)
            
        except KeyboardInterrupt:
            run = False
        except IOError:
            erreurio +=1



        latitude = gpsd.fix.latitude
        longitude = gpsd.fix.longitude
        speed = gpsd.fix.speed
        altitude = gpsd.fix.altitude
        jourheure = gpsd.fix.time
        status =  gpsd.fix.status  #gpsd.fix.status  ou mode
        mode = gpsd.fix.mode
        track = gpsd.fix.track   # Degrees from true north
        climb = gpsd.fix.climb

        titre = "**EasyVine**   lat: " + str(latitude) + "   long: " + str(longitude) + "   cap: " + str(track)+ "   vitesse: " + str(speed) + "   mode: " + str(mode)
        pygame.display.set_caption(titre) 
        ###################################  PERMET D AFFICHER LES VARIABLE QUI CHANGE PENDANT LE COURS DU PRG ###################################


        # permet d'afficher le zoom


        # affiche l'outil en cours


        #####################################################################################################################
        #####################################################################################################################
        ########## C'EST ICI QUE L'ON MET la VRAI POSITION ACTUELLE OU LA POSITION ACTUELLE SIMULéE #########################
        #####################################################################################################################
        # pour effectuer les test j'ai creer un liste de position actuelle et une liste de cap :
        if indice_outil_en_cours == 2 and len(tour_parcelle_gps) > 0: #si on est en mode simulation 
            position_actuelle_gps = tour_parcelle_gps[0] 
            
            
            cap_actuel_gps = 0   # c'est a dire le nord 
        else:
            position_actuelle_gps = (latitude,longitude)           #position_actuelle[i_essai]
            cap_actuel_gps = track    #  cap_actuel[i_essai]


        ## c'est ici que l'on transforme les point gps en point pyg
        ## donc on met un test par rapport au outil
        # mise en place du tour de parcelle
        tour_parcelle_pyg,un_point_pyg, echelle, position_actuelle_pyg = pyg.tour_parcelle(tour_parcelle_gps, position_actuelle_gps,position_actuelle_gps, zoom, centre_x, centre_y, cap_actuel_gps)

        if  indice_outil_en_cours == 0 and  indice_scan_quoi_en_cours == 0:  # c'est l'outil SCAN et on scanne le TOUR PARCELLE
            #if scan_mode_scan == 0:  # VIEW
            #    tour_parcelle_pyg,un_point_pyg, echelle, position_actuelle_pyg = pyg.tour_parcelle(tour_parcelle_gps, position_actuelle_gps,position_actuelle_gps, zoom, centre_x, centre_y, cap_actuel_gps)
            #if scan_mode_scan == 1:  # PAUSE
            #    tour_parcelle_pyg,un_point_pyg, echelle, position_actuelle_pyg = pyg.tour_parcelle(tour_parcelle_gps, position_actuelle_gps,position_actuelle_gps, zoom, centre_x, centre_y, cap_actuel_gps)
            if scan_mode_scan == 2:  # REC
                if len(tour_parcelle_gps) == 0: # si la liste est vide
                    tour_parcelle_gps.append(position_actuelle_gps)  # ajouter la premiere position
                derniere_position_tour_parcelle = tour_parcelle_gps[len(tour_parcelle_gps)-1]
                distance_derniere_position = routine_gps.get_distance_gps(derniere_position_tour_parcelle, position_actuelle_gps)
                if distance_derniere_position > scan_distance_point:
                    tour_parcelle_gps.append(position_actuelle_gps)  # ajouter les position actuelle au tour de la parcelle de la vigne en cours
                #tour_parcelle_pyg,un_point_pyg, echelle, position_actuelle_pyg = pyg.tour_parcelle(tour_parcelle_gps, position_actuelle_gps,position_actuelle_gps, zoom, centre_x, centre_y, cap_actuel_gps)

        ######################  ICI ON SCANNE LES RANGS #############################################
        elif indice_outil_en_cours == 0 and  indice_scan_quoi_en_cours == 1: # ici on scanne les rangs
            #print("scan des rangs")
            # afficher la parcelle
            if  button_state == GPIO.HIGH:         # c'est que l'on n a pas appyuyer sur CLICK FOR SCANNE
                button_state = GPIO.input(button)  # donc on vas chercher l'etat du bouton de la poignet
            if button_state == GPIO.LOW: # ici on a appuyé sur le bouton de la poignet  ou sur le bouton CLICK FOR SCANNE
                #print ("LOW")
                if indice_scan_rang_en_cours == 0: # scanne les debut de rang
                    hauteur = 1
                    #latitude,longitude,hauteur = (latitude,longitude,hauteur)  # je recupere la position dans la liste pour tester
                    position_in_rang = (latitude,longitude,hauteur ) # je commence a preparer les donné pour les rentrer dans le rang
                    occupant_position_in_rang = "AMMARE" # ce sont des ammare qu'il y a en debut de rang
                    etat_occupant_in_rang = "OK" # on par du principe que l'ammare est bonne
                    action_sur_occupant = [] # la liste est vide car car il n'y a rien a faire l'ammare est bonne
                    position_complette_in_rang = [position_in_rang, occupant_position_in_rang,etat_occupant_in_rang,action_sur_occupant] # les donnée sont prete a etre rentre dans le rang en position 0

                    operation_OK, list_rang_vigne = add_debut_rang_in_list_rang(position_complette_in_rang, list_rang_vigne, info_vigne_encours )
                    if operation_OK:
                            position_rang_undo.append(position_complette_in_rang)
                    if operation_OK == False:
                            print("LE DEBUT DE RANG N'A PAS ETE AJOUTER CAR IL EST TROPS PROCHE D'UNE AUTRE DEBUT DE RANG")

                elif indice_scan_rang_en_cours == 1: # scanne les fin de rang
                    position_in_rang = (latitude, longitude, hauteur)  # je commence a preparer les donné pour les rentrer dans le rang
                    occupant_position_in_rang = "AMMARE"  # ce sont des ammare qu'il y a en fin de rang
                    etat_occupant_in_rang = "OK"  # on par du principe que l'ammare est bonne
                    action_sur_occupant = []  # la liste est vide car car il n'y a rien a faire l'ammare est bonne
                    position_complette_in_rang = [position_in_rang, occupant_position_in_rang, etat_occupant_in_rang, action_sur_occupant]  # les donnée sont prete a etre rentre dans le rang en position 0
                    operation_OK, list_rang_vigne = add_fin_rang_in_list_rang(position_complette_in_rang,list_rang_vigne,info_vigne_encours)
                    if operation_OK:
                        position_rang_undo.append(position_complette_in_rang)

                elif indice_scan_rang_en_cours == 2: # scanne les souches
                    pass#                 
                elif indice_scan_rang_en_cours == 1: # scanne les piquets
                    pass
            
            button_state = GPIO.HIGH # sinon on rentre dans une boucle infini ou button_state = GPIO.LOW
        
            
        
        elif indice_outil_en_cours == 3: # outil DK
            if len(list_rang_vigne) > 1:
                print(calculate_distance(position_actuelle_gps, position_rang_in_list(list_rang_vigne,2,0), position_rang_in_list(list_rang_vigne,2,-1)))
                print("outil dk") 





        ######################################  EFFACER L'ECRAN ET AFFICHE SON CONTOUR EN GRIS ##############################################
        pygame.Surface.fill(screen, BLACK)   # a remettre en place apres la fin des test
        # affichage du tour de l'ecran en gris
        pygame.draw.lines(screen, GRAY, True, [(deb_x, deb_y), (fin_x, deb_y), (fin_x, fin_y), (deb_x, fin_y)], 10)

        ################################### AFFICHER LA POSITION ACTUELLE ROND ROUGE  ############################################
        pygame.draw.circle(screen, RED, position_actuelle_pyg, 8)  # long_pyg , lat_pyg

        ################################### AFFICHER LES POINTS GPS TOUR DE LA PARCELLE ###########################################
        for lon_lat in tour_parcelle_pyg:
            
            long_pyg, lat_pyg = lon_lat
            pygame.draw.circle(screen, YELLOW, (long_pyg, lat_pyg), 4)  # long_pyg , lat_pyg
        ################################## AFFICHER LES LIGNES QUI RELIES LES POINT GPS DU TOUR DE LA PARCELLE ###################
        if len(tour_parcelle_pyg) > 1:
            
            pygame.draw.lines(screen, YELLOW, False, tour_parcelle_pyg, 3)
            ######c'est ici que l'on ferme la parcelle  sauf si on est en trai de la scanner
            if scan_mode_scan != 1 and scan_mode_scan !=2: # on n' est pas entrain de scanner donc relier la fin au debut
                pygame.draw.line(screen,YELLOW,tour_parcelle_pyg[0],tour_parcelle_pyg[len(tour_parcelle_pyg) - 1],3)

        #################################  AFFICHER LES POINTS QUI COMPOSE LES RANGS   #############################

        if len(list_rang_vigne) > 0 : # il y a au moins un debut de rang dans la liste
            # transformer les coordonne gps de list_rang_vigne en coordonnée pyg
            list_rang_vigne_pyg,tour_parcelle_pyg,position_actuelle_pyg = pyg.rang_vigne_en_pyg(list_rang_vigne,tour_parcelle_gps, position_actuelle_gps, zoom, centre_x, centre_y, cap_actuel_gps)
            for rang_py in list_rang_vigne_pyg:
                for lon_lat in rang_py:
                    long_pyg, lat_pyg = lon_lat
                    pygame.draw.circle(screen, GREEN, (long_pyg, lat_pyg), 4)  # long_pyg , lat_pyg
                if len(rang_py) > 1:
                    pygame.draw.lines(screen, GREEN, True, rang_py, 3)

        ########################################
        # afficher le bouton vigne
        text_vigne_en_cours = font.render(str(name_vigne_en_cours), True, GREEN, BLUE)  # transformer le texte en graphique
        screen.blit(text_vigne_en_cours, text_vigne_en_coursRect)  # appliquer le texte dans l'ecran
        screen.blit(bouton_vigne_en_cours_d,bouton_chang_vigne_dRect)
        screen.blit(bouton_vigne_en_cours_g, bouton_chang_vigne_gRect)
        screen.blit(libelle_vigne_encours,libelle_vigne_encoursRect)
        screen.blit(bouton_info_vigne_en_cours,bouton_info_vigne_en_coursRect)
        # --
        #affiche les boutton du zoom
        screen.blit(bouton_zoom_g,bouton_zoom_gRect)
        screen.blit(bouton_zoom_d, bouton_zoom_dRect)
        screen.blit(libelle_zoom, libelle_zoomRect)
        screen.blit(text_zoom, text_zoomRect)
        # --
        #affiche les bouton de centrage
        screen.blit(bouton_centre_h,bouton_centre_hRect)
        screen.blit(bouton_centre_d, bouton_centre_dRect)
        screen.blit(bouton_centre_b, bouton_centre_bRect)
        screen.blit(bouton_centre_g, bouton_centre_gRect)
        # --
        #affichage du menu outil
        screen.blit(bouton_outil_en_cours_g, bouton_chang_outil_gRect)
        text_outil_en_cours = font.render(str(name_outil_en_cours), True, GREEN, BLUE)  # transformer le texte en graphique
        screen.blit(text_outil_en_cours, text_outil_en_coursRect)  # appliquer le texte dans l'ecran
        screen.blit(bouton_outil_en_cours_d, bouton_chang_outil_dRect)
        screen.blit(libelle_outil_encours, libelle_outil_encoursRect)
        #########
        # --
        # affichage du menu info_vigne
        if flag_info_vigne:
            screen.blit(libelle_largeur_rang,libelle_largeur_rangRect)
            screen.blit(libelle_distance_cep,libelle_distance_cepRect)
            screen.blit(libelle_cepage,libelle_cepageRect)
            libelle_nb_range = font.render("NB Rangé : " + str(len(list_rang_vigne)), True, WHITE, BLACK)
            screen.blit(libelle_nb_range, libelle_nb_rangeRect)
        ###############################################################################################################
        ###############################         AFFICHAGE DES MENUS OUTILS ############################################

        if indice_outil_en_cours == 0: # SCAN
            name_scan_quoi_en_cours = list_scan_quoi[indice_scan_quoi_en_cours]  # chargement de l'outils
            text_scan_quoi_en_cours = font.render(str(name_scan_quoi_en_cours), True, GREEN, BLUE)  # transformer le texte en graphique
            screen.blit(text_scan_quoi_en_cours,text_scan_quoi_en_coursRect)
            screen.blit(bouton_scan_quoi_g,bouton_scan_quoi_gRect)
            screen.blit(bouton_scan_quoi_d, bouton_scan_quoi_dRect)

            if indice_scan_quoi_en_cours == 0: ### ON EST EN TRAIN DE SCANNER LA PARCELLE
                screen.blit(bouton_rec, bouton_recRect)
                screen.blit(bouton_pause, bouton_pauseRect)
                screen.blit(bouton_undo, bouton_undoRect)
                screen.blit(bouton_redo, bouton_redoRect)
                screen.blit(bouton_view, bouton_viewRect)
                screen.blit(bouton_delete, bouton_deleteRect)
                screen.blit(bouton_save, bouton_saveRect)
                screen.blit(libelle_distance_point, libelle_distance_pointRect)
                screen.blit(bouton_distance_point_g, bouton_distance_point_gRect)
                # affiche la distance entre les point quand on scanne la parcelle
                scan_distance_point = round(scan_distance_point, 2)  # arrondir a 2 decimale pour eviter les erreur infime du a float
                text_scan_distance_point = font.render(format(scan_distance_point, '.2f'), True, GREEN, BLUE)
                screen.blit(text_scan_distance_point, text_scan_distance_pointRect)
                screen.blit(bouton_distance_point_d, bouton_distance_point_dRect)

                bouton_rec = font.render("|  REC  |", True, YELLOW, GRAY)
                bouton_pause = font.render("|PAUSE|", True, YELLOW, GRAY)
                bouton_view = font.render("| VIEW |", True, YELLOW, GRAY)

                if scan_mode_scan == 0: # mode VIEW
                    bouton_rec = font.render("|  REC  |", True, YELLOW, GRAY)
                    bouton_pause = font.render("|PAUSE|", True, YELLOW, GRAY)
                    bouton_view = font.render("| VIEW |", True, YELLOW, RED)

                if scan_mode_scan == 1: # mode PAUSE
                    bouton_rec = font.render("|  REC  |", True, YELLOW, GRAY)
                    bouton_pause = font.render("|PAUSE|", True, YELLOW, RED)
                    bouton_view = font.render("| VIEW |", True, YELLOW, GRAY)

                if scan_mode_scan == 2: # mode REC
                    bouton_rec = font.render("|  REC  |", True, YELLOW, RED)
                    bouton_pause = font.render("|PAUSE|", True, YELLOW, GRAY)
                    bouton_view = font.render("| VIEW |", True, YELLOW, GRAY)

            elif indice_scan_quoi_en_cours == 1: # on est en train de scanner les rangs 
                rang_bouton_debut_rang = font.render(str(list_scan_rang[indice_scan_rang_en_cours]), True, GREEN, BLUE)
                screen.blit(bouton_select_deb_fin_rang_g,bouton_select_deb_fin_rang_gRect)
                screen.blit(bouton_select_deb_fin_rang_d, bouton_select_deb_fin_rang_dRect)
                screen.blit(rang_bouton_debut_rang, rang_bouton_debut_rangRect)
                screen.blit(rang_bouton_enregistre_position, rang_bouton_enregistre_positionRect)
                screen.blit(rang_bouton_undo, rang_bouton_undoRect)
                screen.blit(rang_bouton_redo, rang_bouton_redoRect)
                # screen.blit(bouton_view, bouton_viewRect)
                screen.blit(bouton_delete, bouton_deleteRect)
                screen.blit(bouton_save, bouton_saveRect)
                if indice_scan_rang_en_cours > 1: # onscanne les souche ou les piquets donc possibiité de lier un evenement
                    # ICI METTRE EVENEMENT LIé
                    screen.blit(bouton_evenement_g,bouton_evenement_gRect)
                    screen.blit(bouton_evenement_d,bouton_evenement_dRect)
                    name_evenement_en_cours = list_evenement[indice_list_evenement]  # chargement de l'outils
                    text_evenement_en_cours = font.render(str(name_evenement_en_cours), True, GREEN, BLUE)  # transformer le texte en graphique
                    screen.blit(text_evenement_en_cours,text_evenement_en_coursRect)
                    screen.blit(text_libelle_evenement, text_libelle_evenementRect)


            elif  indice_scan_quoi_en_cours == 2:    # on est en train de scanner les evenements
                screen.blit(rang_bouton_enregistre_position, rang_bouton_enregistre_positionRect)
                screen.blit(rang_bouton_undo, rang_bouton_undoRect)
                screen.blit(rang_bouton_redo, rang_bouton_redoRect)
                screen.blit(bouton_delete, bouton_deleteRect)
                screen.blit(bouton_save, bouton_saveRect)
                

                # ICI METTRE EVENEMENT LIé
                screen.blit(bouton_evenement_g,bouton_evenement_gRect)
                screen.blit(bouton_evenement_d,bouton_evenement_dRect)
                name_evenement_en_cours = list_evenement[indice_list_evenement]  # chargement de l'outils
                text_evenement_en_cours = font.render(str(name_evenement_en_cours), True, GREEN, BLUE)  # transformer le texte en graphique
                screen.blit(text_evenement_en_cours,text_evenement_en_coursRect)
                screen.blit(text_libelle_evenement, text_libelle_evenementRect)

                ################## afficher le niveau ################
                #pygame.draw.lines(screen, GRAY, True, [(deb_x, deb_y), (fin_x, deb_y), (fin_x, fin_y), (deb_x, fin_y)], 10)
                pygame.draw.lines(screen, GRAY, True, [(840, 10), (980, 10), (980, 150), (840, 150)], 5)
                pygame.draw.line(screen,GRAY, (910,10),(910,150) ,4)
                pygame.draw.line(screen,GRAY, (840,80),(980,80) ,4)
                pygame.draw.circle(screen, RED, (911 + roll * 3, 81 + pitch * 3), 10)  # long_pyg , lat_pyg


        elif indice_outil_en_cours == 1: # outil CREAT
            screen.blit(bouton_delete, bouton_deleteRect)
            screen.blit(bouton_save, bouton_saveRect)
            screen.blit(fichier_libelle_nom_vigne, fichier_libelle_nom_vigneRect)
            screen.blit(fichier_libelle_largeur_rang, fichier_libelle_largeur_rangRect)
            screen.blit(fichier_libelle_distance_souche, fichier_libelle_distance_soucheRect)
            screen.blit(fichier_libelle_cepage, fichier_libelle_cepageRect)
            screen.blit(bouton_vigne, bouton_vigneRect)
            screen.blit(bouton_largeur_rang,bouton_largeur_rangRect)
            screen.blit(bouton_distance_souche, bouton_distance_soucheRect)
            screen.blit(bouton_cepage, bouton_cepageRect)

        elif indice_outil_en_cours == 2: # SIMULATION
           # print("simulation dans affichage ecran")
           pass
        elif indice_outil_en_cours == 3: # DK
            print(" DK dans affichage de l'ecran") 
        elif indice_outil_en_cours == 4: # ROBOT
            print("robot dans affichage ecran")
        ###############################################################################################################


        pygame.display.update()





        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                recup_com = pygame.key.name(event.key)   # a voir pour recupere les commande TAB RETURN
                print("recup_com " , recup_com)
                
                recup_touche = event.unicode # pour recuperer les lettre et les chiffre

                
                if len(recup_touche) != 1:
                    recup_touche = "/"
                print(" recup touche : ",recup_touche,"   ord recup touche : ",ord(recup_touche))

                if indice_outil_en_cours == 1:  ################### fichier ##################################
                    if recup_com == "return" or recup_com == "tab":
                        creat_quel_info += 1
                        if creat_quel_info == 4:
                            creat_quel_info = 0

                    if creat_quel_info == 0: # on s'occupe du nom
                        bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, GRAY)
                        bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, GRAY)
                        bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, GRAY)
                        if 94 < ord(recup_touche) < 123 or 64 < ord(recup_touche) <  91 or 47 < ord(recup_touche) < 58: # and (recup_touche) !=  94 :
                            creat_name_vigne = creat_name_vigne+ recup_touche
                        if recup_com == "backspace" or len(creat_name_vigne) == 21:
                            creat_name_vigne = creat_name_vigne[0:-1]
                        bouton_vigne = font.render("|"+creat_name_vigne+"|", True, YELLOW, RED)

                    elif creat_quel_info == 1: # on s'occupe de la largeur du rang
                        bouton_vigne = font.render("|"+creat_name_vigne+"|", True, YELLOW, GRAY)
                        bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, GRAY)
                        bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, GRAY)
                        sortir_point = False
                        if ord(recup_touche) == 46 and creat_largeur_rang.find(".") > -1:
                            sortir_point = True
                        if 47 < ord(recup_touche) < 58 or ord(recup_touche) == 46:
                            creat_largeur_rang = creat_largeur_rang + recup_touche
                        if recup_com == "backspace"  or sortir_point: # bakspace ou si on a ajouter un deuxieme point on le retire
                            creat_largeur_rang = creat_largeur_rang[0:-1]
                        bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, RED)


                    elif creat_quel_info == 2: # on s'occupe de la distance souche
                        bouton_vigne = font.render("|"+creat_name_vigne+"|", True, YELLOW, GRAY)
                        bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, GRAY)
                        bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, GRAY)
                        sortir_point = False
                        if ord(recup_touche) == 46 and creat_distance_souche.find(".") > -1:
                            sortir_point = True
                        if 47 < ord(recup_touche) < 58 or ord(recup_touche) == 46:
                            creat_distance_souche = creat_distance_souche + recup_touche
                        if recup_com == "backspace"  or sortir_point:
                            creat_distance_souche = creat_distance_souche[0:-1]
                        bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, RED)
                    elif creat_quel_info == 3: # on s'occupe du cepage
                        bouton_vigne = font.render("|" + creat_name_vigne + "|", True, YELLOW, GRAY)
                        bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, GRAY)
                        bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, GRAY)
                        if 94 < ord(recup_touche) < 123 or 64 < ord(recup_touche) < 91 or 47 < ord(recup_touche) < 58:  # and (recup_touche) !=  94 :
                            creat_cepage = creat_cepage + recup_touche
                        if recup_com == "backspace"  or len(creat_cepage) == 21:
                            creat_cepage = creat_cepage[0:-1]
                        bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, RED)


            elif event.type == pygame.MOUSEBUTTONDOWN:
                ## SELECTION DE LA VIGNE EN COURS
                if bouton_chang_vigne_gRect.collidepoint(event.pos): # changer de vigne en cours
                    indice_vigne_en_cours, name_vigne_en_cours = preview_vigne(list_vigne, indice_vigne_en_cours)
                    print (chemin_disk + list_vigne[indice_vigne_en_cours])
                    parcelle_tour_et_info = lecture_parcelle(chemin_disk + list_vigne[indice_vigne_en_cours])
                    info_vigne_encours, tour_parcelle_gps = parcelle_tour_et_info
                    list_rang_vigne = lecture_rang(chemin_disk + list_vigne[indice_vigne_en_cours])
                    text_vigne_en_cours = font.render(str(name_vigne_en_cours), True, GREEN,
                                                      BLUE)  # transformer le texte en graphique
                    libelle_largeur_rang = font.render(
                        "largeur rang  : " + format(info_vigne_encours[0], '.2f') + str("M"), True, WHITE, BLACK)
                    libelle_distance_cep = font.render("distance cep  : " + format(info_vigne_encours[1], '.2f') + "M",
                                                       True, WHITE, BLACK)
                    libelle_cepage = font.render("cepage  : " + str(info_vigne_encours[2]), True, WHITE, BLACK)
                    tour_parcelle_pyg = []
                    list_rang_vigne_pyg = []
                    print("NEXT VIGNE  ")
                elif bouton_chang_vigne_dRect.collidepoint(event.pos): # changer de vigne en cours
                    indice_vigne_en_cours, name_vigne_en_cours =  next_vigne(list_vigne, indice_vigne_en_cours)
                    parcelle_tour_et_info = lecture_parcelle(chemin_disk + list_vigne[indice_vigne_en_cours])
                    info_vigne_encours, tour_parcelle_gps = parcelle_tour_et_info
                    list_rang_vigne = lecture_rang(chemin_disk + list_vigne[indice_vigne_en_cours])
                    text_vigne_en_cours = font.render(str(name_vigne_en_cours), True, GREEN,
                                                      BLUE)  # transformer le texte en graphique
                    libelle_largeur_rang = font.render("largeur rang  : " + format(info_vigne_encours[0], '.2f') + str("M"), True, WHITE, BLACK)
                    libelle_distance_cep = font.render("distance cep  : " + format(info_vigne_encours[1], '.2f') + "M",True, WHITE, BLACK)
                    libelle_cepage = font.render("cepage  : " + str(info_vigne_encours[2]), True, WHITE, BLACK)
                    tour_parcelle_pyg = []
                    list_rang_vigne_pyg = []
                if bouton_zoom_gRect.collidepoint(event.pos): #
                    if zoom <= 0.1:
                        if zoom > 0.01:
                            zoom = zoom - 0.01
                    elif zoom <= 1:
                        zoom = zoom - 0.1
                    else:
                        zoom = zoom - 1
                    zoom = round(zoom, 2)  # arrondir a 2 decimale pour eviter les erreur infime du a float
                    text_zoom = font.render(format(zoom, '.2f'), True, GREEN, BLUE)
                elif bouton_zoom_dRect.collidepoint(event.pos): #
                    if zoom <= 0.1:
                        zoom = zoom + 0.01
                    elif zoom <= 1:
                        zoom = zoom + 0.1
                    else:
                        zoom = zoom + 1
                    zoom = round(zoom, 2)  # arrondir a 2 decimale pour eviter les erreur infime du a float
                    text_zoom = font.render(format(zoom, '.2f'), True, GREEN, BLUE)

                if bouton_centre_gRect.collidepoint(event.pos):
                    centre_x = centre_x - 10
                elif bouton_centre_dRect.collidepoint(event.pos):
                    centre_x = centre_x + 10
                elif bouton_centre_bRect.collidepoint(event.pos):
                    centre_y = centre_y + 10
                elif bouton_centre_hRect.collidepoint(event.pos):
                    centre_y = centre_y - 10

                if bouton_chang_outil_gRect.collidepoint(event.pos): # changer de en cours
                    indice_outil_en_cours = indice_outil_en_cours - 1
                    if indice_outil_en_cours == -1 :
                        indice_outil_en_cours = len(list_outil) -1
                    name_outil_en_cours = list_outil[indice_outil_en_cours]  # chargement de la vigne en cours
                    text_outil_en_cours = font.render(str(name_outil_en_cours), True, GREEN,
                                                      BLUE)  # transformer le texte en graphique
                elif bouton_chang_outil_dRect.collidepoint(event.pos): # changer de en cours
                    indice_outil_en_cours = indice_outil_en_cours + 1
                    if indice_outil_en_cours == len(list_outil):
                        indice_outil_en_cours = 0
                    name_outil_en_cours = list_outil[indice_outil_en_cours]  # chargement de la vigne en cours
                    text_outil_en_cours = font.render(str(name_outil_en_cours), True, GREEN,
                                                      BLUE)  # transformer le texte en graphique
                if bouton_info_vigne_en_coursRect.collidepoint(event.pos):
                    if flag_info_vigne == True:
                        flag_info_vigne = False
                    else:
                        flag_info_vigne = True

            #########################################################################
            ################# selectionne dans les menus outil SCAN / DK ######################
                ####
                if indice_outil_en_cours == 0:  ## OUTIL SCAN
                    if bouton_scan_quoi_dRect.collidepoint(event.pos):
                        indice_scan_quoi_en_cours = indice_scan_quoi_en_cours + 1
                        if indice_scan_quoi_en_cours == len(list_scan_quoi):
                            indice_scan_quoi_en_cours = 0
                    if bouton_scan_quoi_gRect.collidepoint(event.pos):
                        indice_scan_quoi_en_cours = indice_scan_quoi_en_cours - 1
                        if indice_scan_quoi_en_cours < 0:
                            indice_scan_quoi_en_cours = len(list_scan_quoi)-1

                    if indice_scan_quoi_en_cours == 0:  ## OUTIL SCAN TOUR DE PARCELLE
                        if bouton_distance_point_gRect.collidepoint(event.pos):
                            if scan_distance_point >= .40:
                                scan_distance_point -= .20
                        if bouton_distance_point_dRect.collidepoint(event.pos):
                            scan_distance_point += .20
                        if bouton_viewRect.collidepoint(event.pos):
                            scan_mode_scan = 0
                        elif bouton_pauseRect.collidepoint(event.pos):
                            scan_mode_scan = 1
                        elif bouton_recRect.collidepoint(event.pos):
                            scan_mode_scan = 2
                        elif bouton_undoRect.collidepoint(event.pos):
                            if len(tour_parcelle_gps) > 1:
                                tour_parcelle_gps_undo.append(tour_parcelle_gps.pop()) # j'enleve le dernier element de tour_parcelle_gps et je le met a la fin de tour_parcelle_gps_undo
                        elif bouton_redoRect.collidepoint(event.pos):
                            if len(tour_parcelle_gps_undo) > 0:
                                tour_parcelle_gps.append((tour_parcelle_gps_undo.pop()))
                        elif bouton_deleteRect.collidepoint(event.pos):
                            tour_parcelle_gps =[]
                            tour_parcelle_gps_undo = []
                            tour_parcelle_pyg = []
                            i_essai = 0
                        elif bouton_saveRect.collidepoint(event.pos):
                            parcelle_tour_et_info = [info_vigne_encours,tour_parcelle_gps]
                            enregistre_parcelle(chemin_disk + list_vigne[indice_vigne_en_cours], parcelle_tour_et_info)
                            screen.blit(alerte_save,alerte_saveRect)
                            pygame.display.update()
                            time.sleep(time_alerte_save)
                ######
                    elif indice_scan_quoi_en_cours == 1:  ## OUTILS SCAN RANG
                        if bouton_select_deb_fin_rang_gRect.collidepoint(event.pos) : # on selectionne si on scanne les debut ou les fin de rang
                            position_rang_redo = []   #mettre les listes vide car on change se que l'on scanne
                            position_rang_undo = []
                            indice_scan_rang_en_cours -= 1
                            if indice_scan_rang_en_cours < 0:
                                indice_scan_rang_en_cours = len(list_scan_rang) -1
                        if  bouton_select_deb_fin_rang_dRect.collidepoint(event.pos):
                            position_rang_redo = []
                            position_rang_undo = []
                            indice_scan_rang_en_cours += 1
                            if indice_scan_rang_en_cours == len(list_scan_rang):
                                indice_scan_rang_en_cours = 0

                        if rang_bouton_enregistre_positionRect.collidepoint(event.pos) and indice_scan_rang_en_cours == 0: # scanne les debut de rang
                            button_state = GPIO.LOW
                            """
                            hauteur = 1
                            #latitude,longitude,hauteur = (latitude,longitude,hauteur)  # je recupere la position dans la liste pour tester
                            position_in_rang = (latitude,longitude,hauteur ) # je commence a preparer les donné pour les rentrer dans le rang
                            occupant_position_in_rang = "AMMARE" # ce sont des ammare qu'il y a en debut de rang
                            etat_occupant_in_rang = "OK" # on par du principe que l'ammare est bonne
                            action_sur_occupant = [] # la liste est vide car car il n'y a rien a faire l'ammare est bonne
                            position_complette_in_rang = [position_in_rang, occupant_position_in_rang,etat_occupant_in_rang,action_sur_occupant] # les donnée sont prete a etre rentre dans le rang en position 0

                            operation_OK, list_rang_vigne = add_debut_rang_in_list_rang(position_complette_in_rang, list_rang_vigne, info_vigne_encours )
                            if operation_OK:
                                position_rang_undo.append(position_complette_in_rang)
                            if operation_OK == False:
                                print("LE DEBUT DE RANG N'A PAS ETE AJOUTER CAR IL EST TROPS PROCHE D'UNE AUTRE DEBUT DE RANG")
                            
                            index_debut_rang += 1 # ce code est pour les essai
                            if index_debut_rang == len(list_debut_rang):
                                index_debut_rang -= 1
                                print("vous avez terminer de rentrez les debut de rang")
                            """

                        elif rang_bouton_enregistre_positionRect.collidepoint(event.pos) and indice_scan_rang_en_cours == 1:  #on sanne les fin de rang
                            button_state = GPIO.LOW
                            #print("j'appuy fin de rang")
                            """
                            #latitude, longitude, hauteur = list_fin_rang[index_fin_rang]  # je recupere la position dans la liste d'essai pour tester
                            position_in_rang = (latitude, longitude, hauteur)  # je commence a preparer les donné pour les rentrer dans le rang
                            occupant_position_in_rang = "AMMARE"  # ce sont des ammare qu'il y a en fin de rang
                            etat_occupant_in_rang = "OK"  # on par du principe que l'ammare est bonne
                            action_sur_occupant = []  # la liste est vide car car il n'y a rien a faire l'ammare est bonne
                            position_complette_in_rang = [position_in_rang, occupant_position_in_rang,
                                                          etat_occupant_in_rang,
                                                          action_sur_occupant]  # les donnée sont prete a etre rentre dans le rang en position 0

                            operation_OK, list_rang_vigne = add_fin_rang_in_list_rang(position_complette_in_rang,list_rang_vigne,info_vigne_encours)
                            if operation_OK:
                                position_rang_undo.append(position_complette_in_rang)
                            
                            index_fin_rang += 1 # ce code est pour les essai
                            if index_fin_rang == len(list_fin_rang):
                                index_fin_rang -= 1
                                print("vous avez terminer de rantrez les debut de rang")   bouton_evenement_gRect

                            """
                        elif rang_bouton_enregistre_positionRect.collidepoint(event.pos) and indice_scan_rang_en_cours == 2:#SOUCHE SCAN
                            button_state = GPIO.LOW
                            

                        elif rang_bouton_enregistre_positionRect.collidepoint(event.pos) and indice_scan_rang_en_cours == 3:#PIQUET SCAN
                            button_state = GPIO.LOW    


                        elif rang_bouton_undoRect.collidepoint(event.pos) and len(position_rang_undo) > 0:
                            position_complette_undo = position_rang_undo.pop()
                            position_rang_redo.append(position_complette_undo)
                            undo_in_list_rang_vigne(position_complette_undo, list_rang_vigne)
                        elif rang_bouton_redoRect.collidepoint(event.pos) and len(position_rang_redo) > 0:
                            position_complette_in_rang = position_rang_redo.pop()
                            position_rang_undo.append(position_complette_in_rang)
                            if indice_scan_rang_en_cours == 0: # redo sur debut de rang
                                operation_OK, list_rang_vigne = add_debut_rang_in_list_rang(position_complette_in_rang, list_rang_vigne, info_vigne_encours )
                            elif indice_scan_rang_en_cours == 1: # redo sur fin de rang
                                operation_OK, list_rang_vigne = add_fin_rang_in_list_rang(position_complette_in_rang,
                                                                                          list_rang_vigne,
                                                                                          info_vigne_encours)
                        elif bouton_deleteRect.collidepoint(event.pos):
                            list_rang_vigne = []
                        elif bouton_saveRect.collidepoint(event.pos):
                            print("SAVE RANG  ", list_vigne[indice_vigne_en_cours])
                            enregistre_rang(chemin_disk + list_vigne[indice_vigne_en_cours], list_rang_vigne)
                            screen.blit(alerte_save,alerte_saveRect)
                            pygame.display.update()
                            time.sleep(time_alerte_save)

                        # les evenements
                        elif (indice_scan_rang_en_cours == 2 or indice_scan_rang_en_cours == 3 ) and bouton_evenement_gRect.collidepoint(event.pos):
                            indice_list_evenement -= 1
                            if indice_list_evenement < 0:
                                indice_list_evenement = len(list_evenement) - 1   
                        elif (indice_scan_rang_en_cours == 2 or indice_scan_rang_en_cours == 3 ) and bouton_evenement_dRect.collidepoint(event.pos):
                            indice_list_evenement += 1
                            if indice_list_evenement == len(list_evenement):
                                indice_list_evenement = 0    

                    elif indice_scan_quoi_en_cours == 2 :  ## OUTILS SCAN evenement
                        if bouton_evenement_gRect.collidepoint(event.pos):
                            indice_list_evenement -= 1
                            if indice_list_evenement < 0:
                                indice_list_evenement = len(list_evenement) - 1   
                        elif bouton_evenement_dRect.collidepoint(event.pos):
                            indice_list_evenement += 1
                            if indice_list_evenement == len(list_evenement):
                                indice_list_evenement = 0 

                            

                elif indice_outil_en_cours == 1: # fichier OUTIL FICHIER


                    list_rang_vigne =[]
                    name_vigne_en_cours = ""
                    tour_parcelle_gps = []
                    tour_parcelle_pyg = []
                    info_vigne_encours = [0,0,"pas de cepage"]
                    parcelle_tour_et_info = [info_vigne_encours, tour_parcelle_gps]
                    libelle_largeur_rang = font.render("largeur rang  : " + format(info_vigne_encours[0], '.2f') + str("M"), True, WHITE, BLACK)
                    libelle_distance_cep = font.render("distance cep  : " + format(info_vigne_encours[1], '.2f') + "M", True, WHITE, BLACK)
                    libelle_cepage = font.render("cepage  : " + str(info_vigne_encours[2]), True, WHITE, BLACK)

                    if bouton_vigneRect.collidepoint(event.pos):
                        creat_quel_info = 0  #print ("je rentre le nom de la vigne")
                        bouton_vigne = font.render("|" + creat_name_vigne+ "|", True, YELLOW, RED)
                        bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, GRAY)
                        bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, GRAY)
                        bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, GRAY)
                    elif bouton_largeur_rangRect.collidepoint(event.pos):
                        creat_quel_info = 1  # print("je rentre la largeur du rang")
                        bouton_vigne = font.render("|" + creat_name_vigne+ "|", True, YELLOW, GRAY)
                        bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, RED)
                        bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, GRAY)
                        bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, GRAY)
                    elif bouton_distance_soucheRect.collidepoint(event.pos):
                        creat_quel_info = 2 # print("je rentre la distance souche")
                        bouton_vigne = font.render("|" + creat_name_vigne+ "|", True, YELLOW, GRAY)
                        bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, GRAY)
                        bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, RED)
                        bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, GRAY)
                    elif bouton_cepageRect.collidepoint(event.pos):
                        creat_quel_info = 3
                        bouton_vigne = font.render("|" + creat_name_vigne+ "|", True, YELLOW, GRAY)
                        bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, GRAY)
                        bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, GRAY)
                        bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, RED)
                    elif bouton_deleteRect.collidepoint(event.pos): # je remet les information a rien
                        creat_quel_info = 0
                        creat_name_vigne = ""
                        creat_largeur_rang = ""
                        creat_distance_souche = ""
                        creat_cepage = ""
                        bouton_vigne = font.render("|" + creat_name_vigne + "|", True, YELLOW, RED)
                        bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, GRAY)
                        bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, GRAY)
                        bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, GRAY)

                    elif bouton_saveRect.collidepoint(event.pos): # je creer un nouveau fichier vigne
                        if creat_name_vigne != "" and creat_largeur_rang != "" and creat_distance_souche != "" and creat_cepage != "":
                            print(list_vigne)
                            if creat_name_vigne in list_vigne:
                                print("la vigne  existe   : ")
                            else: # sauvegarde
                                print("je sauve la vigne")
                                info_vigne_encours = [float(creat_largeur_rang), float(creat_distance_souche),creat_cepage]
                                parcelle_tour_et_info = [info_vigne_encours, tour_parcelle_gps]
                                enregistre_parcelle(chemin_disk + creat_name_vigne, parcelle_tour_et_info )
                                enregistre_rang(chemin_disk + creat_name_vigne, list_rang_vigne)
                                list_vigne.append(creat_name_vigne)
                                creat_name_vigne = ""
                                creat_largeur_rang = ""
                                creat_distance_souche = ""
                                creat_cepage = ""
                                creat_quel_info = 0
                                bouton_vigne = font.render("|" + creat_name_vigne + "|", True, YELLOW, RED)
                                bouton_largeur_rang = font.render("|" + creat_largeur_rang + "|", True, YELLOW, GRAY)
                                bouton_distance_souche = font.render("|" + creat_distance_souche + "|", True, YELLOW, GRAY)
                                bouton_cepage = font.render("|" + creat_cepage + "|", True, YELLOW, GRAY)
                                screen.blit(alerte_save,alerte_saveRect)
                                pygame.display.update()
                                time.sleep(time_alerte_save)

                elif indice_outil_en_cours == 2: # outil simulation
                    print("outil simulation ", indice_outil_en_cours)
                    
                elif indice_outil_en_cours == 3: # dk
                    print("outil DK ", indice_outil_en_cours)
                    
                elif indice_outil_en_cours == 4: # robot
                    pass

print ("\nKilling Thread...")
gpsp.running = False
gpsp.join() # wait for the thread to finish what it's doing
pygame.quit()
print('quitter le prg' )
pygame.quit()