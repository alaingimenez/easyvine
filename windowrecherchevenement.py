# windowrecherchevenement




TIME_MSG = 1
import config
import main
import routine_gps
#import routine_robot
import robot
import windowalerte
import pyg
from communication import*
#from routine_vigne import*

from operator import itemgetter
import time
import pygame
pygame.init()
"""
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(config.PIN_NO_RTK,GPIO.IN, pull_up_down = GPIO.PUD_UP)
"""

#import gpiozero
# no_rtk = gpiozero.Button(PIN_NO_RTK, pull_up= False)  dans se cas pull_up est DOWN


#no_rtk = gpiozero.Button(config.PIN_NO_RTK)

# buton_scan = gpiozero.Button(config.PIN_BUTON_SCAN)

import sys




class WindowRecherchEvenement:
    def __init__(self, window_m, module, parcel):

        self.window_main = window_m
        self.screen = self.window_main.screen
        self.module = module
        self.parcel = parcel
        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet
        self.robot = robot.Robot()
        
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_mg = pygame.font.Font('freesansbold.ttf', 30)
        self.font_g = pygame.font.Font('freesansbold.ttf', 80)

        self.flag_info = False

        self.libelle_saving = self.font_g.render("** SAVING **", True, config.GREEN, config.GRAY)
        self.libelle_savingRect = self.libelle_saving.get_rect()
        self.libelle_savingRect.x = 400
        self.libelle_savingRect.y = 400

        self.position_gps = (0, 0)
        self.position_gps_simule = (0,0)
        self.latitude = 0
        self.longitude = 0
        self.pitch = 0
        self.roll = 0
        self.track = 0
        self.track_simule = 0
        self.altitude = 0

        self.position_py = (0,0)
        self.tour_parcelle_pyg =[]
        self.vigne_pyg = []
        self.evenement_pyg = []
        self.parcour_pyg = []
        

        
        self.vitesse_simule_a = 0.01 # permette de faire varier la vitesse du parcour
        self.vitesse_simule_b = 0.1
        
        self.distance_detection = float(self.parcel.largeur_rang) / 2

        self.event_selected = []
        

        self.ligne_vigne = [] # contient les lignes entre les rangs pour reperer les evenement sou la forme ligne_vigne = [[(lon,lat),(lon,lat)], [(lon,lat),(lon,lat)]]
        self.ligne_vigne_pyg = []
        self.ligne_event = []
        self.ligne_event_pyg = []
        self.ligne_vigne_event = []
        self.index_evenement_proche = 0

        if len(self.parcel.vigne) > 0:
            self.premier_rang = self.parcel.vigne[0] 
        self.cap_parcours = 0
        self.cap_inverse_parcours = 0


        self.buton_state = 1




        

        
        self.buton_arbre = self.font_mg.render("|ARBRE|", True, config.couleur_arbre, config.GRAY)
        self.buton_arbreRect = self.buton_arbre.get_rect()
        self.buton_arbreRect.x = 10
        self.buton_arbreRect.y = 80
        self.buton_arbre_actif= False

        self.buton_racine = self.font_mg.render("|RACINE|", True, config.couleur_racine, config.GRAY)
        self.buton_racineRect = self.buton_racine.get_rect()
        self.buton_racineRect.x = 150
        self.buton_racineRect.y = 80
        self.buton_racine_actif = False

        self.buton_mort = self.font_mg.render("|MORT|", True, config.couleur_mort, config.GRAY)
        self.buton_mortRect = self.buton_mort.get_rect()
        self.buton_mortRect.x = 300
        self.buton_mortRect.y = 80
        self.buton_mort_actif = False

        self.buton_americain = self.font_mg.render("|AMERICAIN|", True, config.couleur_americain, config.GRAY)
        self.buton_americainRect = self.buton_americain.get_rect()
        self.buton_americainRect.x = 420
        self.buton_americainRect.y = 80
        self.buton_americain_actif = False

        self.buton_espalier = self.font_mg.render("|ESPALIER|", True, config.couleur_espalier, config.GRAY)
        self.buton_espalierRect = self.buton_espalier.get_rect()
        self.buton_espalierRect.x = 620
        self.buton_espalierRect.y = 80
        self.buton_espalier_actif = False

        self.buton_pulve = self.font_mg.render("|PULVE|", True, config.couleur_pulve, config.GRAY)
        self.buton_pulveRect = self.buton_pulve.get_rect()
        self.buton_pulveRect.x = 790
        self.buton_pulveRect.y = 80
        self.buton_pulve_actif = False

        self.buton_rabassier = self.font_mg.render("|RABASSIER|", True, config.couleur_rabassier, config.GRAY)
        self.buton_rabassierRect = self.buton_rabassier.get_rect()
        self.buton_rabassierRect.x = 910
        self.buton_rabassierRect.y = 80
        self.buton_rabassier_actif = False

        self.nb_event_selected = self.font.render("NB evenement selectionné : " + str(len(self.event_selected)), True, config.WHITE, config.BLACK)
        self.nb_event_selectedRect = self.nb_event_selected.get_rect()
        self.nb_event_selectedRect.x = 1000
        self.nb_event_selectedRect.y = 120

        

        #############################################
        #############################################
        # format(self.parcel.largeur_rang, '.2f')
        self.libelle_largeur_rang = self.font.render("largeur rang  : " + str( self.parcel.largeur_rang) + "M" , True, config.WHITE, config.BLACK)
        self.libelle_largeur_rangRect = self.libelle_largeur_rang.get_rect() #font.render(format(zoom, '.2f')
        self.libelle_largeur_rangRect.x = 10
        self.libelle_largeur_rangRect.y = 400

        # format(self.parcel.distance_souche, '.2f')
        self.libelle_distance_cep = self.font.render("distance cep  : "+ str(self.parcel.distance_souche) +"M", True, config.WHITE, config.BLACK)
        self.libelle_distance_cepRect = self.libelle_distance_cep.get_rect()
        self.libelle_distance_cepRect.x = 10
        self.libelle_distance_cepRect.y = 440

        self.libelle_cepage = self.font.render("cepage  : "+ self.parcel.cepage , True, config.WHITE, config.BLACK)
        self.libelle_cepageRect = self.libelle_cepage.get_rect()
        self.libelle_cepageRect.x = 10
        self.libelle_cepageRect.y = 480

        self.libelle_nb_range = self.font.render("NB Rangé : " + str(len(self.parcel.vigne)), True, config.WHITE, config.BLACK)
        self.libelle_nb_rangeRect = self.libelle_nb_range.get_rect()
        self.libelle_nb_rangeRect.x = 20
        self.libelle_nb_rangeRect.y = 520

        self.libelle_nb_event = self.font.render("NB evenement : " + str(len(self.parcel.evenement)), True, config.WHITE, config.BLACK)
        self.libelle_nb_eventRect = self.libelle_nb_event.get_rect()
        self.libelle_nb_eventRect.x = 20
        self.libelle_nb_eventRect.y = 560


        self.update()

    def update(self):
        self.screen.blit(self.buton_arbre, self.buton_arbreRect)
        self.screen.blit(self.buton_racine, self.buton_racineRect)
        self.screen.blit(self.buton_mort, self.buton_mortRect)
        self.screen.blit(self.buton_americain, self.buton_americainRect)
        self.screen.blit(self.buton_espalier, self.buton_espalierRect)
        self.screen.blit(self.buton_pulve, self.buton_pulveRect)
        self.screen.blit(self.buton_rabassier, self.buton_rabassierRect)
        self.nb_event_selected = self.font.render("NB evenement selectionné : " + str(len(self.event_selected)), True, config.WHITE, config.BLACK)
        self.screen.blit(self.nb_event_selected, self.nb_event_selectedRect)
        

        #####################################
        #####################################
        if self.flag_info:
            l_r = float(self.parcel.largeur_rang)
            self.libelle_largeur_rang = self.font.render("largeur rang  : " + format( l_r, '.2f') + "M" , True, config.WHITE, config.BLACK)
            self.screen.blit(self.libelle_largeur_rang, self.libelle_largeur_rangRect)
            d_t = float(self.parcel.distance_souche)
            self.libelle_distance_cep = self.font.render("distance cep  : "+ format( d_t, '.2f') +"M", True, config.WHITE, config.BLACK)
            self.screen.blit(self.libelle_distance_cep , self.libelle_distance_cepRect )
            self.libelle_cepage = self.font.render("cepage  : "+ self.parcel.cepage , True, config.WHITE, config.BLACK)
            self.screen.blit(self.libelle_cepage , self.libelle_cepageRect )
            self.libelle_nb_range = self.font.render("NB Rangé : " + str(len(self.parcel.vigne)), True, config.WHITE, config.BLACK)
            self.screen.blit(self.libelle_nb_range , self.libelle_nb_rangeRect )
            self.libelle_nb_event = self.font.render("NB evenement : " + str(len(self.parcel.evenement)), True, config.WHITE, config.BLACK)
            self.screen.blit(self.libelle_nb_event , self.libelle_nb_eventRect )

    
    def creer_parcours(self):
        self.module.flag_parcours = True

        #regarder ou se trouve le robot et tourner la vigne pour que le premier rang de la liste soit pret du robot
        self.robot.position = self.position_gps
        pos_robot = self.robot.robot_a_cote(self.parcel.vigne) # retrouver la position du robot par rapport a la vigne
        self.parcel.reverse_vigne(pos_robot) # tourner la vigne de maniere a ce que la liste est la premiere rangé a cote du robot
        
        self.ligne_vigne = [] # contient les lignes entre les rangs pour reperer les evenement sou la forme ligne_vigne = [[(lon,lat),(lon,lat)], [(lon,lat),(lon,lat)]]
        self.ligne_vigne_pyg = []
        self.ligne_event = []
        self.ligne_event_pyg = []
        self.ligne_vigne_event = []
        
        # savoir de quel coté s'etale la vigne droite ou gauche -1 = un seul rang / 1 = a droite / 0 = a gauche
        cote = self.parcel.vigne_setend()
        index_ligne_event = 0
        if cote == 1: # la vigne s'etend a droite
            ofset_cap = -90
        elif cote == 0: # la vigne s'etend a gauche
            ofset_cap = 90
        elif cote == -1: # il n'y a q'une seule range
            print("parcour pour vigne a une rangé non calculé")
            # si il n y a qu'une seule rangé regarder de quel coté est le robot et renvoyer cote = a 1 ou 0
            # selon le cote ou est le robot
            return

        rang = self.parcel.vigne[0] 
        cap, cap_inverse = self.parcel.cap_rang(rang)
        # CREER LA PREMIERE LIGNE A L'EXTERIEUR DE LA VIGNE
        pos_debut,quoi,an,hauteur,arrosage,travail = rang [0] # premiere ammare premier rang
        pos_fin,quoi,an,hauteur,arrosage,travail = rang [-1]  # derniere ammare premier rang
        demi_largeur = float(self.parcel.largeur_rang) / 2
        ad_dep = routine_gps.new_pointgpt(routine_gps.new_pointgpt(pos_debut, cap + ofset_cap, demi_largeur), cap_inverse, self.robot.longueur)
        ad_fin = routine_gps.new_pointgpt(routine_gps.new_pointgpt(pos_fin, cap + ofset_cap, demi_largeur), cap, self.robot.longueur )

        # attribuer les evenement a la ligne 0
        for ev in self.event_selected:
            point,nom = ev
            if routine_gps.calculate_distance(point, ad_dep, ad_fin) <= demi_largeur:
                self.ligne_event.append(ev)
        if len(self.ligne_event) > 0:
            self.ligne_vigne_event.append(self.ligne_event)    
            self.ligne_vigne.append([ad_dep, ad_fin])

            index_ligne_event += 1

        # CREER LES LIGNE QUI S'ETENDE VERS LA DROITE et attribuer les evenements
        for rang in self.parcel.vigne:
            pos_debut,quoi,an,hauteur,arrosage,travail = rang [0] # premiere ammare premier ran
            pos_fin,quoi,an,hauteur,arrosage,travail = rang [-1]  # derniere ammare premier rang
            ad_dep = routine_gps.new_pointgpt(routine_gps.new_pointgpt(pos_debut, cap + (ofset_cap * -1), demi_largeur), cap_inverse, self.robot.longueur)
            ad_fin = routine_gps.new_pointgpt(routine_gps.new_pointgpt(pos_fin, cap + (ofset_cap * -1), demi_largeur), cap, self.robot.longueur )
            #
            # atribuer les evenement a la ligne encours
            self.ligne_event = []
            for ev in self.event_selected:
                point,nom = ev
                if routine_gps.calculate_distance(point, ad_dep, ad_fin) <= demi_largeur:
                    # verifier si ev est deja present dans les lignes precedent si oui ne pas le rajouter
                    exist = False
                    for lng in self.ligne_vigne_event:
                        for ev_compar in lng:
                            if ev_compar == ev:
                                exist = True # l'evenement existe
                    if exist == False:            
                        self.ligne_event.append(ev)
            if len(self.ligne_event) > 0:
                self.ligne_vigne_event.append(self.ligne_event)    
                self.ligne_vigne.append([ad_dep, ad_fin])
                print("LIGNE evenement n° ",index_ligne_event)
                print (self.ligne_event)
                index_ligne_event += 1

        # commencer a preparer le parcours il faut inverser les adresse debut fin sur les lignes impaire pour avoir la coutinuité du parcours
        index = 0
        print("AVANT")
        print(self.ligne_vigne)
        for ligne in self.ligne_vigne:
            if (index % 2) != 0:
                ad_dep, ad_fin = ligne
                self.ligne_vigne[index] = [ad_fin, ad_dep]
            index += 1    
        print("APRES")
        print(self.ligne_vigne)        


        # pour controle imprimer les evenement et leur index de ligne
        for index in range(len(self.ligne_vigne)):
            print("index ",index)
            print(self.ligne_vigne_event[index])  
        
        # attribuer la distance de chaque evenement avec le debut de la ligne
        ligne_vigne_distance_evenement = []
        for index in range(len(self.ligne_vigne)):
            debut, fin = self.ligne_vigne[index]
            ligne_distance_evenement = []
            for li_ev in self.ligne_vigne_event[index]:
                point,nom = li_ev
                distance = routine_gps.get_distance_gps(point, debut)
                ligne_distance_evenement.append((distance, li_ev))
            ligne_vigne_distance_evenement.append(ligne_distance_evenement)   
        print ("ligne_vigne_distance_evenement") 
        print(ligne_vigne_distance_evenement)    

        # trier chaque ligne d'evenement par rappor a la distance du debut de ligne
        for index in range(len(self.ligne_vigne)):
            print(" ligne_vigne_distance_evenement[index]", index)
            print ( ligne_vigne_distance_evenement[index])
            #ligne_vigne_distance_evenement[index] = sorted.ligne_vigne_distance_evenement[index]
            ligne_vigne_distance_evenement[index] = sorted(ligne_vigne_distance_evenement[index], key=itemgetter(0), reverse=False)
        print ("ligne_vigne_distance_evenement TRIER") 
        print(ligne_vigne_distance_evenement) 
        
        # remettre les evenements trier dans self.event_selected
        self.event_selected = []
        for index in range(len(self.ligne_vigne)):
            for dis_ev in ligne_vigne_distance_evenement[index]:
                distance, ev = dis_ev
                self.event_selected.append(ev)

        # transformer les lignes en parcours        
        self.robot.parcour = []
        self.robot.parcour.append(self.position_gps)
        for ad in self.ligne_vigne:
            debut, fin = ad
            self.robot.parcour.append(debut)
            self.robot.parcour.append(fin)

                




       
        

    def position_amarre(self, indice, distance):
        """
        return un point gps qui sert a positionner le robot avant la creation du parcour pendant la simulation
            si indice = 1 return la position de la premiere amarre du premier rang
            si indice = 2 return la position de la derniere amarre du premier rang 
            si indice = 3 return la position de la derniere amarre du dernier rang
            si indice = 4 return la position de la premiere amarre du dernier rang

        """
        if  len(self.parcel.vigne) > 0: # le tour de la parcelle est existant donc initialiser  self.position_gps_simule
            rang = self.parcel.vigne[0]
            cap, cap_inverse = self.parcel.cap_rang(rang)
            position,quoi,an,hauteur,arrosage,travail = rang[0]

            if indice == 1: # on simule que le gps est au  point de la liste premier rang premier amarre
                self.position_gps_simule = routine_gps.new_pointgpt(position, cap_inverse, distance)
                self.track_simule = cap
                 
            elif indice == 2: # on simule que le gps est au  point de la liste premier rang dernier amarre
                position,quoi,an,hauteur,arrosage,travail = rang[-1]
                self.position_gps_simule = routine_gps.new_pointgpt(position, cap, distance)
                self.track_simule = cap_inverse
                
            elif indice == 3: # on simule que le gps est au point de la liste dernier rang dernier amarre 
                rang = self.parcel.vigne[-1]
                position,quoi,an,hauteur,arrosage,travail = rang[-1]                
                self.position_gps_simule = routine_gps.new_pointgpt(position, cap, distance)
                self.track_simule = cap_inverse
                   
            elif indice == 4: #  numero 4 # on simule que le gps est au point de la liste dernier rang premier amarre 
                rang = self.parcel.vigne[-1]
                #print(rang)
                position,quoi,an,hauteur,arrosage,travail = rang[0]
                self.position_gps_simule = routine_gps.new_pointgpt(position, cap_inverse, distance)
                self.track_simule = cap
            return 

    def reset_parcour_et_ligne(self):
        self.evenement_pyg = []
        self.parcour_pyg = []
        self.robot.parcour = []
        self.ligne_vigne_pyg = []
        self.ligne_vigne = []
        self.module.flag_parcours = False

    def deselectionne_event(self):
        self.buton_arbre_actif = False
        self.buton_arbre = self.font_mg.render("|ARBRE|", True, config.couleur_arbre, config.GRAY)
        self.buton_racine_actif = False
        self.buton_racine = self.font_mg.render("|RACINE|", True, config.couleur_racine, config.GRAY)
        self.buton_mort_actif = False
        self.buton_mort = self.font_mg.render("|MORT|", True, config.couleur_mort, config.GRAY)
        self.buton_americain_actif = False
        self.buton_americain = self.font_mg.render("|AMERICAIN|", True, config.couleur_americain, config.GRAY)
        self.buton_espalier_actif = False
        self.buton_espalier = self.font_mg.render("|ESPALIER|", True, config.couleur_espalier, config.GRAY)
        self.buton_pulve_actif = False
        self.buton_pulve = self.font_mg.render("|PULVE|", True, config.couleur_pulve, config.GRAY)
        self.buton_rabassier_actif = False
        self.buton_rabassier = self.font_mg.render("|RABASSIER|", True, config.couleur_rabassier, config.GRAY)
        self.event_selected = [] 
        self.evenement_pyg = [] 

    def valide_reparation(self):
        self.reset_parcour_et_ligne()
        print("VALIDER LES REPARATIONS")
        print("nombre d evenement self.parcel.evenement ", len(self.parcel.evenement))
        # print(self.parcel.evenement)
        #self.parcel.evenement = self.enleve_doublon_liste(self.parcel.evenement)
        evenement_repare = False
        for ev in self.event_selected:
            pos,name = ev
            if name == "REPARE":
                evenement_repare = True
        
        
         

        if evenement_repare: # des evenement on ete reparer donc demmander si on veux valider
            self.windowalerte = windowalerte.WindowAlerte(self.screen, "voulez vous valider les reparations ","des evenements")  # creer la fenetre d'alerte
            if self.windowalerte.update():  # attente de reponse de la fenetre d'alerte
                print("windowalerte OUI JE VALIDE LES REPARATION")

                for ev_select in self.event_selected:
                    pos_select,name = ev_select
                    
                    if name == "REPARE":
                        #print("element a reparer pos_select ", pos_select)

                        index_a_detruire = -1
                        for index in range (len(self.parcel.evenement)):
                            
                            pos_parcel,rien = self.parcel.evenement[index]
                            #print("pos_select  ", pos_select, "pos_parcel ", pos_parcel, "rien ", rien)

                            if pos_select == pos_parcel:
                                #print("c'est un index adetruire ")

                                index_a_detruire = index
                                
                        if index_a_detruire != -1:
                            del(self.parcel.evenement[index_a_detruire])
         

                # il faut encore sauvegarder
                self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                
                self.deselectionne_event()
                self.reset_parcour_et_ligne()

                
            else:
                print("NON JE NE VALIDE PAS LES REPARATION")
     

     
    def enleve_doublon_liste(self, liste):
        new_list = []
        for el in liste:
            if el in new_list:
                pass
            else:
                new_list.append(el)
        return new_list



    def gestion(self):########### EVENEMENT #########
        gs = main.GpsPoller()
        gs.start() # start it up

        """
        buton = 4  #  c'est le bouton qui est sur le manche a droite et qui permet de scanner les rangs
        GPIO.setup(buton, GPIO.IN, GPIO.PUD_UP)
        self.buton_state = GPIO.HIGH
        """
        self.buton_state = 1

        erreurio = 0

        if  len(self.parcel.tour) > 0: # le tour de la parcelle est existant donc initialiser  self.position_gps_simule
                self.position_gps_simule = self.parcel.tour[0] # on simule que le gps est au premier point de la parcelle

       
        
       
        while True:
            #if(GPIO.input(config.PIN_NO_RTK)):
            if  not config.NO_RTK.is_pressed: 
                rtk = "**"
            else:
                rtk = "RTK oK **"

            titre = rtk +"EasyVine RECHERCHE EVENEMENT **   lat: " + format(self.latitude, '.7f') + "   long: " + format(self.longitude, '.7f') + "  track: " + format(self.track,'.2f') + "  altitude: " + format(self.altitude, '.4f') 
            pygame.display.set_caption(titre) 
           
            pygame.Surface.fill(self.screen, config.BLACK)
            # c'est ici que je vais affficher les parcelle et les rang

            ################################### AFFICHER LA POSITION ACTUELLE ROND ROUGE  ############################################
            pygame.draw.circle(self.screen, config.RED, self.position_py, 8)  # long_pyg , lat_pyg

            ################################### AFFICHER LES POINTS GPS TOUR DE LA PARCELLE ###########################################
            for lon_lat in self.tour_parcelle_pyg:
                long_pyg, lat_pyg = lon_lat
                pygame.draw.circle(self.screen, config.YELLOW, (long_pyg, lat_pyg), 4)  # long_pyg , lat_pyg

            ################################## AFFICHER LES LIGNES QUI RELIES LES POINT GPS DU TOUR DE LA PARCELLE ###################
            if len(self.tour_parcelle_pyg) > 1:
                pygame.draw.lines(self.screen, config.YELLOW, True, self.tour_parcelle_pyg, 3)

            #################################  AFFICHER LES POINTS et LES LIGNES QUI COMPOSE LES RANGS   #############################
            if len(self.parcel.vigne) > 0: # il y a au moins un debut de rang
                for rang_py in self.vigne_pyg:
                    for lon_lat in rang_py:
                        long_pyg, lat_pyg = lon_lat
                        pygame.draw.circle(self.screen, config.GREEN, (long_pyg, lat_pyg), 4)  # long_pyg , lat_pyg
                    if len(rang_py) > 1:
                        pygame.draw.lines(self.screen, config.GREEN, True, rang_py, 3)

            ################################ AFFICHER LE PARCOURS ######################################
            #
            
            if len(self.parcour_pyg) > 0:
                pygame.draw.lines(self.screen, config.CITROUILLE, False, (self.position_py  ,self.parcour_pyg[0]), 6)
            if len(self.parcour_pyg) > 1:
                pygame.draw.lines(self.screen, config.CITROUILLE, False, self.parcour_pyg, 6)
            ################################    POUR LES ESSAIS ########################################
            ############################ AFFICHER LES LIGNES ENTRE LES RANGS POUR REPERER LES EVENEMENTS ##################
            #
            #for line in self.ligne_vigne_pyg:
            #    pygame.draw.lines(self.screen, config.BLUE, True, line, 3)


            ###############################################################################################################
            ###############################################################################################################

            
            ############################ AFFICHER LES EVENEMENTS #######################################
            # 
            if len(self.event_selected) > 0:
                self.index_evenement_proche = -1 # pas d'evenement selectionnné
                index = 0
                for evenement in self.evenement_pyg:
                    lon_lat, nom = evenement
                    long_pyg, lat_pyg = lon_lat
                    
                    # entoure et selectionner l'evenement le plus proche
                    pos_gps,name = self.event_selected[index]
                    if routine_gps.get_distance_gps(pos_gps, self.position_gps ) < self.distance_detection: # si l'evenement est a moins de 1 mettre 
                        pygame.draw.circle(self.screen, config.WHITE, (long_pyg, lat_pyg), 12)  # long_pyg , lat_pyg
                        self.index_evenement_proche = index # retenir l'evenement selectionné le mettre a REPARE par la suite

                    
                    if nom == "ARBRE":
                        couleur = config.couleur_arbre
                    elif nom == "RACINE":
                        couleur = config.couleur_racine   
                    elif nom == "MORT":
                        couleur = config.couleur_mort
                    elif nom == "AMERICAIN":
                        couleur = config.couleur_americain
                    elif nom == "ESPALIER":
                        couleur = config.couleur_espalier
                    elif nom == "PULVE":
                        couleur = config.couleur_pulve
                    elif nom == "RABASSIER":
                        couleur = config.couleur_rabassier 
                    elif nom == "REPARE":
                        couleur = config.BLACK 

                    pygame.draw.circle(self.screen, couleur, (long_pyg, lat_pyg), 8)  # long_pyg , lat_pyg


                    index +=1
                    

                        


            ########################################### AFFICHE LES MENUS ##############################
            self.window_main.update()  # # affiche a l'ecran les texte
            self.module.update()
            self.update()
            pygame.display.update()



            ####################################################################################################
            ###############   CALCULER ET suivre le parcours et eliminer les evenement traité   ################
            ####################################################################################################
            #self.robot.parcour   self.position_gps
            #self.event_selected
            # modifier l'adresse de parcour[0] en le raprochant de parcour[1]
            # mesurer la distance et le track entre parcour[0] et parcour[1]
            # si inferieur a 0.1M detruire la premiere adresse du parcour[0]

             
            """
            if len(self.robot.parcour) > 0:

                self.robot.parcour[0] = routine_gps.new_pointgpt(self.robot.parcour[0], self.track_simule, 0.03)
                if routine_gps.get_distance_gps(self.robot.parcour[0], self.robot.parcour[1] ) < 0.20: # 0.1
                    del(self.robot.parcour[0])
                    if len(self.robot.parcour) == 1:
                        self.robot.parcour = []
            """

                    
                    





            try:
                self.pitch = read_pitch()
                self.roll = read_roll()
            except IOError:
                erreurio += 1

            self.latitude = gs.gpsd.fix.latitude
            self.longitude = gs.gpsd.fix.longitude
            self.position_gps = (self.latitude, self.longitude)
            self.track = gs.gpsd.fix.track
            self.altitude_gps = gs.gpsd.fix.altitude

            
            ################ MODE SIMULATION  ##########################
            # modifier l'adresse de parcour[0] en le raprochant de parcour[1]
            # mesurer la distance et le track entre parcour[0] et parcour[1]
            # si inferieur a 0.1M detruire la premiere adresse du parcour[0]
            if self.module.mode_simulation: # and len(self.parcel.tour) > 0: 
                if len(self.robot.parcour) > 1:
                    if self.module.simulation_arret == False: # permet d'arreter le parcour quand on appuy sur le bouton vitesse
                        self.track_simule = routine_gps.get_angle(self.robot.parcour[0], self.robot.parcour[1])
                        self.position_gps_simule = routine_gps.new_pointgpt(self.robot.parcour[0], self.track_simule, self.vitesse_simule_a )#0.01
                        self.robot.parcour[0] = routine_gps.new_pointgpt(self.robot.parcour[0], self.track_simule, self.vitesse_simule_a )
                        if routine_gps.get_distance_gps(self.robot.parcour[0], self.robot.parcour[1] ) < self.vitesse_simule_b: # 0.1
                            del(self.robot.parcour[0])
                            if len(self.robot.parcour) == 1: # le parcour est terminer donc initialiser
                                self.reset_parcour_et_ligne()
                                self.valide_reparation() # demmander si on valide les reparation car le parcour est terminé                     
                self.position_gps = self.position_gps_simule # on simule que le gps est au premier point de la parcelle
                self.track = self.track_simule  #  
            else: ################ MODE REEL  ##########################
                if len(self.robot.parcour) > 0:
                    if routine_gps.get_distance_gps(self.position_gps, self.robot.parcour[0]) < float(self.parcel.largeur_rang) / 2 :
                        del(self.robot.parcour[0])
                        if len(self.robot.parcour) == 0: # le parcour est terminer donc initialiser
                            self.reset_parcour_et_ligne()
                            self.valide_reparation() # demmander si on valide les reparation car le parcour est terminé


            if  self.buton_state == 1:         # c'est que l'on n a pas appyuyer sur CLICK FOR SCANNE
                if config.BUTON_SCAN.is_pressed:      # donc on vas chercher l'etat du bouton de la poignet
                    self.buton_state = 0 
            if self.buton_state == 0: # ici on a appuyé sur le bouton de la poignet  ou sur le bouton CLICK FOR SCANNE
                # ici on peut faire un action si l'on appuy sur le bouton poignet
                #print("JE FAIS UNE ACTION ")
                self.buton_state = 1 # sinon on rentre dans une boucle infini ou button_state = GPIO.LOW
            #print("self.buton_state : ",self.buton_state)
            









            ###################### TRANSFORMER LES COORDONNEES GPS EN COORDONNE PYG ##############################


            self.parcour_pyg, self.evenement_pyg, self.vigne_pyg, self.tour_parcelle_pyg, un_point, echelle, self.position_py = pyg.gps_en_pyg(
                                                                                        self.robot.parcour, self.event_selected, 
                                                                                        self.parcel.vigne,
                                                                                        self.parcel.tour, self.position_gps,
                                                                                        self.position_gps, self.window_main.zoom, 
                                                                                        self.window_main.centre_x,
                                                                                        self.window_main.centre_y, self.track)
            """
            #########################################################################################################
            ################# POUR LES TESTS
            #               POUR LES TEST TRANSFORMER LES LIGNES QUI REPERE LES EVENEMENTS
            self.ligne_vigne_pyg = []
            for ligne in self.ligne_vigne:
                new_line = []
                for ad in ligne:
                    self.parcour_pyg, self.evenement_pyg, self.vigne_pyg, self.tour_parcelle_pyg, ad_pyg, echelle, self.position_py = pyg.gps_en_pyg(
                                                                                        self.robot.parcour, self.event_selected, 
                                                                                        self.parcel.vigne,
                                                                                        self.parcel.tour, self.position_gps,
                                                                                        ad, self.window_main.zoom, 
                                                                                        self.window_main.centre_x,
                                                                                        self.window_main.centre_y, self.track)
                    new_line.append(ad_pyg)
                self.ligne_vigne_pyg.append(new_line)
                                                                            
            """


           



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.valide_reparation() # demmander si on valide les reparation avant de quiter
                    self.window_main.index_action = -99 # permet de fermer le programe
                    gs.running = False
                    gs.join() # wait for the thread to finish what it's doing
                    del(gs)
                    return 0  # return windowrecherch
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # ICI gerer les evenements de cette fenetre 
                    if self.module.flag_parcours == False:
                        if self.buton_arbreRect.collidepoint(event.pos):
                            if self.buton_arbre_actif:
                                self.buton_arbre_actif = False
                                self.buton_arbre = self.font_mg.render("|ARBRE|", True, config.couleur_arbre, config.GRAY)
                                list_new =[]
                                for ev in self.event_selected: # sortir les arbres de la liste self.event_selected
                                    if ev[1] != "ARBRE":
                                        list_new.append(ev)
                                self.event_selected = list_new 
                                self.evenement_pyg = [] 
                            else:
                                self.buton_arbre_actif = True
                                self.buton_arbre = self.font_mg.render("|ARBRE|", True, config.couleur_arbre, config.RED)
                                for ev in self.parcel.evenement: # ajouter les arbres a la liste self.event_selected
                                    if ev[1] == "ARBRE":
                                        self.event_selected.append(ev)      
                            
                        elif self.buton_racineRect.collidepoint(event.pos):
                            if self.buton_racine_actif:
                                self.buton_racine_actif = False
                                self.buton_racine = self.font_mg.render("|RACINE|", True, config.couleur_racine, config.GRAY)
                                list_new =[]
                                for ev in self.event_selected: # sortir les racine
                                    if ev[1] != "RACINE":
                                        list_new.append(ev)
                                self.event_selected = list_new
                                self.evenement_pyg = []  
                            else:
                                self.buton_racine_actif = True
                                self.buton_racine = self.font_mg.render("|RACINE|", True, config.couleur_racine, config.RED)
                                for ev in self.parcel.evenement:
                                    if ev[1] == "RACINE":
                                        self.event_selected.append(ev) 
                                         

                        elif self.buton_mortRect.collidepoint(event.pos):
                            if self.buton_mort_actif:
                                self.buton_mort_actif = False
                                self.buton_mort = self.font_mg.render("|MORT|", True, config.couleur_mort, config.GRAY)
                                list_new =[]
                                for ev in self.event_selected:
                                    if ev[1] != "MORT":
                                        list_new.append(ev)
                                self.event_selected = list_new 
                                self.evenement_pyg = []  
                            else:
                                self.buton_mort_actif = True
                                self.buton_mort = self.font_mg.render("|MORT|", True, config.couleur_mort, config.RED)
                                for ev in self.parcel.evenement:
                                    if ev[1] == "MORT":
                                        self.event_selected.append(ev) 
                            
                        elif self.buton_americainRect.collidepoint(event.pos):
                            if self.buton_americain_actif:
                                self.buton_americain_actif = False
                                self.buton_americain = self.font_mg.render("|AMERICAIN|", True, config.couleur_americain, config.GRAY)
                                list_new =[]
                                for ev in self.event_selected:
                                    if ev[1] != "AMERICAIN":
                                        list_new.append(ev)
                                self.event_selected = list_new 
                                self.evenement_pyg = []  
                            else:
                                self.buton_americain_actif = True
                                self.buton_americain = self.font_mg.render("|AMERICAIN|", True, config.couleur_americain, config.RED)
                                for ev in self.parcel.evenement:
                                    if ev[1] == "AMERICAIN":
                                        self.event_selected.append(ev) 
                            
                        elif self.buton_espalierRect.collidepoint(event.pos):
                            if self.buton_espalier_actif:
                                self.buton_espalier_actif = False
                                self.buton_espalier = self.font_mg.render("|ESPALIER|", True, config.couleur_espalier, config.GRAY)
                                list_new =[]
                                for ev in self.event_selected:
                                    if ev[1] != "ESPALIER":
                                        list_new.append(ev)
                                self.event_selected = list_new 
                                self.evenement_pyg = []  
                            else:
                                self.buton_espalier_actif = True
                                self.buton_espalier = self.font_mg.render("|ESPALIER|", True, config.couleur_espalier, config.RED)
                                for ev in self.parcel.evenement:
                                    if ev[1] == "ESPALIER":
                                        self.event_selected.append(ev) 
                            
                        elif self.buton_pulveRect.collidepoint(event.pos):
                            if self.buton_pulve_actif:
                                self.buton_pulve_actif = False
                                self.buton_pulve = self.font_mg.render("|PULVE|", True, config.couleur_pulve, config.GRAY)
                                list_new =[]
                                for ev in self.event_selected:
                                    if ev[1] != "PULVE":
                                        list_new.append(ev)
                                self.event_selected = list_new 
                                self.evenement_pyg = []  
                            else:
                                self.buton_pulve_actif = True
                                self.buton_pulve = self.font_mg.render("|PULVE|", True, config.couleur_pulve, config.RED)
                                for ev in self.parcel.evenement:
                                    if ev[1] == "PULVE":
                                        self.event_selected.append(ev) 
                            
                        elif self.buton_rabassierRect.collidepoint(event.pos):
                            if self.buton_rabassier_actif:
                                self.buton_rabassier_actif = False
                                self.buton_rabassier = self.font_mg.render("|RABASSIER|", True, config.couleur_rabassier, config.GRAY)
                                list_new =[]
                                for ev in self.event_selected:
                                    if ev[1] != "RABASSIER":
                                        list_new.append(ev)
                                self.event_selected = list_new 
                                self.evenement_pyg = []  
                            else:
                                self.buton_rabassier_actif = True
                                self.buton_rabassier = self.font_mg.render("|RABASSIER|", True, config.couleur_rabassier, config.RED)
                                for ev in self.parcel.evenement:
                                    if ev[1] == "RABASSIER":
                                        self.event_selected.append(ev) 
                        

                        




                    ##-----------------------------------------------------------
                    ##-----------------------------------------------------------
                    ########## GERE LES EVENEMENTS DE LA windowrecherch module
                    if self.module.buton_simuRect.collidepoint(event.pos): # BUTON 
                        if self.module.mode_simulation:
                            self.module.mode_simulation = False
                        else:
                            self.module.mode_simulation = True
                            if  len(self.parcel.tour) > 0: # le tour de la parcelle est existant donc initialiser  self.position_gps_simule
                                self.position_gps_simule = self.parcel.tour[0] # on simule que le gps est au premier point de la parcelle
                                self.track_simule = 0
                    elif self.module.buton_parcoursRect.collidepoint(event.pos): # BUTON 
                        self.module.buton_libelle_vitesse = self.font.render(str(self.module.indice_vitesse), True, config.YELLOW, config.RED)
                        self.creer_parcours()
                    elif self.module.buton_plus_viteRect.collidepoint(event.pos):
                        if self.module.indice_vitesse < 20:        
                            self.module.indice_vitesse += 1 
                        self.vitesse_simule_a = self.module.indice_vitesse /100 
                        self.vitesse_simule_b = self.module.indice_vitesse /10 
                    elif self.module.buton_moins_viteRect.collidepoint(event.pos):
                        if self.module.indice_vitesse > 1:        
                            self.module.indice_vitesse -= 1
                        self.vitesse_simule_a = self.module.indice_vitesse /100 
                        self.vitesse_simule_b = self.module.indice_vitesse /10 
                    elif self.module.buton_libelle_vitesseRect.collidepoint(event.pos):
                        if self.module.simulation_arret:
                            self.module.simulation_arret = False
                        else:
                            self.module.simulation_arret = True

                    elif self.module.buton_repareRect.collidepoint(event.pos):
                        if self.index_evenement_proche != -1 and len(self.event_selected) > 0: # ça veut dire qu'un evenement est proche
                            pos,name = self.event_selected[self.index_evenement_proche] 
                            self.event_selected[self.index_evenement_proche] = [pos,"REPARE"]

                    elif self.module.buton_valid_repareRect.collidepoint(event.pos):
                        self.valide_reparation()     

                    elif self.module.buton_clearRect.collidepoint(event.pos):
                        self.deselectionne_event()
                        self.reset_parcour_et_ligne()    
                        
                    elif self.module.buton_bgRect.collidepoint(event.pos):
                        self.position_amarre(1, 1) # premiere rang premier amarre a 1 metre
                        self.reset_parcour_et_ligne()
                    elif self.module.buton_hgRect.collidepoint(event.pos):
                        self.position_amarre(2, 1) # premier rang dernier amarre a 1 metre
                        self.reset_parcour_et_ligne()
                    elif self.module.buton_hdRect.collidepoint(event.pos):
                        self.position_amarre(3, 1) # dernier rang dernier amarre a 1 metre
                        self.reset_parcour_et_ligne()
                    elif self.module.buton_bdRect.collidepoint(event.pos):
                        self.position_amarre(4, 1) # dernier rang premiere amarre a 1 metre
                        self.reset_parcour_et_ligne()
                        
                           

                    

                    ########## ON RETURN AU FICHIER windowscan POUR CHANGER DE MODULE ###########
                    elif self.module.buton_gRect.collidepoint(event.pos):
                        return -1 # on return au fichier windowscan.py pour changer de module
                    elif self.module.buton_dRect.collidepoint(event.pos):
                        return 1  # on return au fichier windowscan.py pour changer de module

                    ###########################################################
                    ########## GERE LES EVENEMENTS DE LA window.main ##########
                    ###########################################################
                    ########## flag_info
                    elif self.window_main.buton_infoRect.collidepoint(event.pos):
                        if self.flag_info:
                            self.flag_info = False
                        else:
                            self.flag_info = True 
                    ########## CHANGEMENT DE PARCELLE #################
                    elif self.window_main.bouton_parcelle_gRect.collidepoint(event.pos):  # change de parcelle
                        #self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.valide_reparation()
                        self.event_selected = []
                        self.deselectionne_event()
                        self.reset_parcour_et_ligne()
                        self.window_main.dec_index_parcelle()
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet
                        if  len(self.parcel.tour) > 0: # le tour de la parcelle est existant donc initialiser  self.position_gps_simule
                                self.position_gps_simule = self.parcel.tour[0] # on simule que le gps est au premier point de la parcelle
                                self.track_simule = 0
                        print("type ",type(self.parcel))
                        
                    elif self.window_main.bouton_parcelle_dRect.collidepoint(event.pos):  # change de parcelle
                        #self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.valide_reparation()
                        self.event_selected = []
                        self.deselectionne_event()
                        self.reset_parcour_et_ligne()
                        self.window_main.inc_index_parcelle()
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet
                        if  len(self.parcel.tour) > 0: # le tour de la parcelle est existant donc initialiser  self.position_gps_simule
                                self.position_gps_simule = self.parcel.tour[0] # on simule que le gps est au premier point de la parcelle
                                self.track_simule = 0
                        print("type ",type(self.parcel))

                    retour = self.window_main.gest_event(event, self.parcel)
                    if retour == 0 : # si l'ACTION change return a windowscan et return a main.py 
                        self.valide_reparation()
                        return 0


                