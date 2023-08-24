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

import time
import pygame
pygame.init()

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


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

        self.mode_simulation = True
        self.event_selected = []

        self.buton_state = GPIO.HIGH




        

        
        self.buton_arbre = self.font_mg.render("|ARBRE|", True, config.couleur_arbre, config.GRAY)
        self.buton_arbreRect = self.buton_arbre.get_rect()
        self.buton_arbreRect.x = 10
        self.buton_arbreRect.y = 60
        self.buton_arbre_actif= False

        self.buton_racine = self.font_mg.render("|RACINE|", True, config.couleur_racine, config.GRAY)
        self.buton_racineRect = self.buton_racine.get_rect()
        self.buton_racineRect.x = 150
        self.buton_racineRect.y = 60
        self.buton_racine_actif = False

        self.buton_mort = self.font_mg.render("|MORT|", True, config.couleur_mort, config.GRAY)
        self.buton_mortRect = self.buton_mort.get_rect()
        self.buton_mortRect.x = 300
        self.buton_mortRect.y = 60
        self.buton_mort_actif = False

        self.buton_americain = self.font_mg.render("|AMERICAIN|", True, config.couleur_americain, config.GRAY)
        self.buton_americainRect = self.buton_americain.get_rect()
        self.buton_americainRect.x = 420
        self.buton_americainRect.y = 60
        self.buton_americain_actif = False

        self.buton_espalier = self.font_mg.render("|ESPALIER|", True, config.couleur_espalier, config.GRAY)
        self.buton_espalierRect = self.buton_espalier.get_rect()
        self.buton_espalierRect.x = 620
        self.buton_espalierRect.y = 60
        self.buton_espalier_actif = False

        self.buton_pulve = self.font_mg.render("|PULVE|", True, config.couleur_pulve, config.GRAY)
        self.buton_pulveRect = self.buton_pulve.get_rect()
        self.buton_pulveRect.x = 790
        self.buton_pulveRect.y = 60
        self.buton_pulve_actif = False

        self.buton_rabassier = self.font_mg.render("|RABASSIER|", True, config.couleur_rabassier, config.GRAY)
        self.buton_rabassierRect = self.buton_rabassier.get_rect()
        self.buton_rabassierRect.x = 790
        self.buton_rabassierRect.y = 100
        self.buton_rabassier_actif = False

        self.nb_event_selected = self.font.render("NB evenement selectionné : " + str(len(self.event_selected)), True, config.WHITE, config.BLACK)
        self.nb_event_selectedRect = self.nb_event_selected.get_rect()
        self.nb_event_selectedRect.x = 10
        self.nb_event_selectedRect.y = 100

        

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
        print(self.event_selected)
        #regarder ou se trouve le robot et tourner la vigne pour que le premier rang de la liste soit pret du robot
        self.robot.position = self.position_gps
        pos_robot = self.robot.robot_a_cote(self.parcel.vigne)
        self.parcel.reverse_vigne(pos_robot) # 

        rang = self.parcel.vigne[0] 
        cap, cap_inverse = self.parcel.cap_rang(rang)

        # savoir de quel coté s'etale la vigne droite ou gauche -1 = un seul rang / 1 = a droite / 0 = a gauche
        cote = self.parcel.vigne_setend()
        if cote == 1: # la vigne s'etend a droite
            pos_debut,quoi,an,hauteur,arrosage,travail = rang[0]
            pos_fin,quoi,an,hauteur,arrosage,travail = rang[-1]
            demi_largeur = float(self.parcel.largeur_rang) / 2
            ad_dep = routine_gps.new_pointgpt(routine_gps.new_pointgpt(pos_debut, cap - 90, demi_largeur), cap_inverse, self.robot.longueur)
            ad_fin = routine_gps.new_pointgpt(routine_gps.new_pointgpt(pos_fin, cap - 90, demi_largeur), cap, self.robot.longueur )
            self.robot.parcour.append(ad_dep)
            self.robot.parcour.append(ad_fin)
            print("parcour ", self.robot.parcour)
            # creer un point a gauche debut de rang et fin de rang et a 1/2 rang et les mettre a l'exterieur de la vigne
            # de la longueur du robot
            pass
        elif cote == 0: # la vigne s'etend a gauche
            pass
        elif cote == -1: # il n'y a q'une seule range
            pass
        # tracer des ligne entre chaque rangé et a mis distance
        #tracer une ligne a mis distance de la premiere range a l'extrieur de la vigne
        #tracer une ligne a mis distance de la derniere range et a mis distance
        #rallonger les lignes de la longueur robot
        #regarder la distance de l'evenement a la ligne si la distances est inferieure a une 1/2 rangé attribuer
        #l'evenement a cette ligne
        #
        # pour les tests recuperer un adresse gps a chaque bout des rang exterieur
        

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


    def gestion(self):########### EVENEMENT #########
        gs = main.GpsPoller()
        gs.start() # start it up

        buton = 4  #  c'est le bouton qui est sur le manche a droite et qui permet de scanner les rangs
        GPIO.setup(buton, GPIO.IN, GPIO.PUD_UP)
        self.buton_state = GPIO.HIGH

        erreurio = 0

        if  len(self.parcel.tour) > 0: # le tour de la parcelle est existant donc initialiser  self.position_gps_simule
                self.position_gps_simule = self.parcel.tour[0] # on simule que le gps est au premier point de la parcelle

        while True:
            titre = "**EasyVine RECHERCHE EVENEMENT **   lat: " + format(self.latitude, '.7f') + "   long: " + format(self.longitude, '.7f') + "  track: " + format(self.track,'.2f') + "  altitude: " + format(self.altitude, '.4f')
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

            #################################  AFFICHER LES POINTS QUI COMPOSE LES RANGS   #############################
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
                pygame.draw.lines(self.screen, config.BLUE, True, self.parcour_pyg, 3)

            
            ############################ AFFICHER LES EVENEMENTS #######################################
            # 
            if len(self.evenement_pyg) > 0:
                for evenement in self.evenement_pyg:
                    lon_lat, nom = evenement
                    long_pyg, lat_pyg = lon_lat
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

                    pygame.draw.circle(self.screen, couleur, (long_pyg, lat_pyg), 8)  # long_pyg , lat_pyg
                    

                        


            ########################################### AFFICHE LES MENUS ##############################
            self.window_main.update()  # # affiche a l'ecran les texte
            self.module.update()
            self.update()
            pygame.display.update()



            ####################################################################################################
            ###############   CALCULER ET suivre le parcours et eliminer les evenement traité   ################
            ####################################################################################################


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

            
            if self.mode_simulation: # and len(self.parcel.tour) > 0: # le tour de la parcelle est existant est mode VIEW
                self.position_gps = self.position_gps_simule # on simule que le gps est au premier point de la parcelle
                self.track = self.track_simule  #  



            if  self.buton_state == GPIO.HIGH:         # c'est que l'on n a pas appyuyer sur CLICK FOR SCANNE
                self.buton_state = GPIO.input(buton)  # donc on vas chercher l'etat du bouton de la poignet
            if self.buton_state == GPIO.LOW: # ici on a appuyé sur le bouton de la poignet  ou sur le bouton CLICK FOR SCANNE
                # ici on peut faire un action si l'on appuy sur le bouton poignet
                self.buton_state = GPIO.HIGH # sinon on rentre dans une boucle infini ou button_state = GPIO.LOW

            









            ###################### TRANSFORMER LES COORDONNEES GPS EN COORDONNE PYG ##############################


            self.parcour_pyg, self.evenement_pyg, self.vigne_pyg, self.tour_parcelle_pyg, un_point, echelle, self.position_py = pyg.gps_en_pyg(
                                                                                        self.robot.parcour, self.event_selected, 
                                                                                        self.parcel.vigne,
                                                                                        self.parcel.tour, self.position_gps,
                                                                                        self.position_gps, self.window_main.zoom, 
                                                                                        self.window_main.centre_x,
                                                                                        self.window_main.centre_y, self.track)



           



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.windowalerte = windowalerte.WindowAlerte(self.screen, "voulez vous sauvegarder la vigne ","de la parcelle")  # creer la fenetre d'alerte
                    if self.windowalerte.update():  # attente de reponse de la fenetre d'alerte
                        self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                    self.window_main.index_action = -99 # permet de fermer le programe
                    gs.running = False
                    gs.join() # wait for the thread to finish what it's doing
                    del(gs)
                    return 0  # return windowrecherch
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # ICI gerer les evenements de cette fenetre 
                    if self.buton_arbreRect.collidepoint(event.pos):
                        
                        if self.buton_arbre_actif:
                            self.buton_arbre_actif = False
                            self.buton_arbre = self.font_mg.render("|ARBRE|", True, config.couleur_arbre, config.GRAY)
                            list_new =[]
                            for ev in self.event_selected:
                                if ev[1] != "ARBRE":
                                    list_new.append(ev)
                            self.event_selected = list_new  
                        else:
                            self.buton_arbre_actif = True
                            self.buton_arbre = self.font_mg.render("|ARBRE|", True, config.couleur_arbre, config.RED)
                            for ev in self.parcel.evenement:
                                if ev[1] == "ARBRE":
                                    self.event_selected.append(ev)      
                        
                    elif self.buton_racineRect.collidepoint(event.pos):
                        if self.buton_racine_actif:
                            self.buton_racine_actif = False
                            self.buton_racine = self.font_mg.render("|RACINE|", True, config.couleur_racine, config.GRAY)
                            list_new =[]
                            for ev in self.event_selected:
                                if ev[1] != "RACINE":
                                    list_new.append(ev)
                            self.event_selected = list_new  
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
                        else:
                            self.buton_rabassier_actif = True
                            self.buton_rabassier = self.font_mg.render("|RABASSIER|", True, config.couleur_rabassier, config.RED)
                            for ev in self.parcel.evenement:
                                if ev[1] == "RABASSIER":
                                    self.event_selected.append(ev) 
                        

                        




                    ##-----------------------------------------------------------
                    ##-----------------------------------------------------------
                    ########## GERE LES EVENEMENTS DE LA windowrecherch module
                    elif self.module.buton_simuRect.collidepoint(event.pos): # BUTON 
                        if self.mode_simulation:
                            self.mode_simulation = False
                            self.module.buton_simu = self.font.render("|SIMU|", True, config.YELLOW, config.GRAY)
                        else:
                            self.mode_simulation = True
                            self.module.buton_simu = self.font.render("|SIMU|", True, config.YELLOW, config.RED)
                            if  len(self.parcel.tour) > 0: # le tour de la parcelle est existant donc initialiser  self.position_gps_simule
                                self.position_gps_simule = self.parcel.tour[0] # on simule que le gps est au premier point de la parcelle
                                self.track_simule = 0
                    elif self.module.buton_parcoursRect.collidepoint(event.pos): # BUTON 
                        print("MODULE A IMPLEMENTER  PARCOURS")
                        self.creer_parcours()
                        
                            
                    elif self.module.buton_delRect.collidepoint(event.pos):
                        print("MODULE A IMPLEMENTER")
                        """
                        self.windowalerte = windowalerte.WindowAlerte(self.screen, "voulez vous detruire tous les evenements ",self.window_main.name_parcelle)  # creer la fenetre d'alerte
                        if self.windowalerte.update():  # attente de reponse de la fenetre d'alerte
                            self.parcel.evenement = []
                            self.evenement_pyg = []
                            #self.list_undo.append(self.parcel.tour.pop())
                        """
                    elif self.module.buton_saveRect.collidepoint(event.pos):
                        print("id parcel :", id(self.parcel))
                        self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        print("id parcel :", id(self.parcel))
                        self.screen.blit(self.libelle_saving, self.libelle_savingRect)
                        pygame.display.update()
                        time.sleep(TIME_MSG)

                    elif self.module.buton_bgRect.collidepoint(event.pos):
                        self.position_amarre(1, 1) # premiere rang premier amarre a 1 metre
                        self.parcour_pyg = []
                        self.robot.parcour = []
                    elif self.module.buton_hgRect.collidepoint(event.pos):
                        self.position_amarre(2, 1) # premier rang dernier amarre a 1 metre
                        self.parcour_pyg = []
                        self.robot.parcour = []
                    elif self.module.buton_hdRect.collidepoint(event.pos):
                        self.position_amarre(3, 1) # dernier rang dernier amarre a 1 metre
                        self.parcour_pyg = []
                        self.robot.parcour = []
                    elif self.module.buton_bdRect.collidepoint(event.pos):
                        self.position_amarre(4, 1) # dernier rang premier amarre a 1 metre
                        self.parcour_pyg = []
                        self.robot.parcour = []
                        
                           

                    

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
                        self.evenement_pyg = []
                        self.window_main.dec_index_parcelle()
                        
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet
                        
                    elif self.window_main.bouton_parcelle_dRect.collidepoint(event.pos):  # change de parcelle
                        #self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.evenement_pyg = []
                        self.window_main.inc_index_parcelle()
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet

                    retour = self.window_main.gest_event(event, self.parcel)
                    if retour == 0 : # si l'ACTION change return a windowscan et return a main.py 
                        return 0


                