# windowview
BLACK = (0, 0, 0)
GRAY = (206, 206, 206) #(127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

ALEZAN = (167, 103, 38)
AMBRE = (240, 195, 0)
FER = (132, 132, 132)
CHROME = (255, 255, 5)
CITROUILLE = (223, 109, 20)
BLEU = (0, 0, 255)

couleur_arbre = WHITE
couleur_racine = MAGENTA
couleur_mort = CHROME
couleur_americain = GREEN
couleur_espalier = FER
couleur_pulve = ALEZAN
couleur_rabassier = BLEU


TIME_MSG = 1

import main
import routine_gps
import windowalerte
import pyg
from communication import*
from routine_vigne import*
import parcelle


import time
import pygame
pygame.init()

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


import sys



class WindowView:
    def __init__(self, window_m):

        self.window_main = window_m
        self.screen = self.window_main.screen

        self.parcel = parcelle.Parcelle
        
        #print("id parcel :", id(self.parcel))
        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet


        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_mg = pygame.font.Font('freesansbold.ttf', 50)
        self.font_g = pygame.font.Font('freesansbold.ttf', 80)

        self.flag_info = False

        self.position_gps = (0, 0)
        self.latitude = 0
        self.longitude = 0
        self.pitch = 0
        self.roll = 0
        self.track = 0
        self.altitude = 0

        self.position_py = (0,0)
        self.tour_parcelle_pyg =[]
        self.vigne_pyg = []
        self.evenement_pyg = []

        self.arbre = 0
        self.racine = 0
        self.mort = 0
        self.americain = 0
        self.espalier = 0
        self.pulve = 0
        self.rabassier = 0
        self.count_evenement()

        


        width = 780
        width1 = 740

        self.libelle_general = self.font.render("evenement general", True, WHITE, BLACK)
        self.libelle_generalRect = self.libelle_general.get_rect()
        self.libelle_generalRect.x = 700
        self.libelle_generalRect.y = 20

        self.buton_arbre = self.font.render("|ARBRE|", True, couleur_arbre, BLACK)
        self.buton_arbreRect = self.buton_arbre.get_rect()
        self.buton_arbreRect.x = width
        self.buton_arbreRect.y = 60

        self.nb_arbre = self.font.render(str(self.arbre), True, couleur_arbre, BLACK)
        self.nb_arbreRect = self.nb_arbre.get_rect()
        self.nb_arbreRect.x = width1
        self.nb_arbreRect.y = 60

        self.buton_racine = self.font.render("|RACINE|", True, couleur_racine, BLACK)
        self.buton_racineRect = self.buton_racine.get_rect()
        self.buton_racineRect.x = width
        self.buton_racineRect.y = 100

        self.nb_racine = self.font.render(str(self.racine), True, couleur_racine, BLACK)
        self.nb_racineRect = self.nb_racine.get_rect()
        self.nb_racineRect.x = width1
        self.nb_racineRect.y = 100

        self.buton_mort = self.font.render("|MORT|", True, couleur_mort, BLACK)
        self.buton_mortRect = self.buton_mort.get_rect()
        self.buton_mortRect.x = width
        self.buton_mortRect.y = 140

        self.nb_mort = self.font.render(str(self.mort), True, couleur_mort, BLACK)
        self.nb_mortRect = self.nb_mort.get_rect()
        self.nb_mortRect.x = width1
        self.nb_mortRect.y = 140

        self.buton_americain = self.font.render("|AMERICAIN|", True, couleur_americain, BLACK)
        self.buton_americainRect = self.buton_americain.get_rect()
        self.buton_americainRect.x = width
        self.buton_americainRect.y = 180

        self.nb_americain = self.font.render(str(self.americain), True, couleur_americain, BLACK)
        self.nb_americainRect = self.nb_americain.get_rect()
        self.nb_americainRect.x = width1
        self.nb_americainRect.y = 180

        self.buton_espalier = self.font.render("|ESPALIER|", True, couleur_espalier, BLACK)
        self.buton_espalierRect = self.buton_espalier.get_rect()
        self.buton_espalierRect.x = width
        self.buton_espalierRect.y = 220

        self.nb_espalier = self.font.render(str(self.espalier), True, couleur_espalier, BLACK)
        self.nb_espalierRect = self.nb_espalier.get_rect()
        self.nb_espalierRect.x = width1
        self.nb_espalierRect.y = 220

        self.buton_pulve = self.font.render("|PULVE|", True, couleur_pulve, BLACK)
        self.buton_pulveRect = self.buton_pulve.get_rect()
        self.buton_pulveRect.x = width
        self.buton_pulveRect.y = 260

        self.nb_pulve = self.font.render(str(self.pulve), True, couleur_pulve, BLACK)
        self.nb_pulveRect = self.nb_pulve.get_rect()
        self.nb_pulveRect.x = width1
        self.nb_pulveRect.y = 260

        self.buton_rabassier = self.font.render("|RABASSIER|", True, couleur_rabassier, BLACK)
        self.buton_rabassierRect = self.buton_rabassier.get_rect()
        self.buton_rabassierRect.x = width
        self.buton_rabassierRect.y = 300

        self.nb_rabassier = self.font.render(str(self.rabassier), True, couleur_rabassier, BLACK)
        self.nb_rabassierRect = self.nb_rabassier.get_rect()
        self.nb_rabassierRect.x = width1
        self.nb_rabassierRect.y = 300

        self.libelle_plant = self.font.render("travaux plant", True, WHITE, BLACK)
        self.libelle_plantRect = self.libelle_plant.get_rect()
        self.libelle_plantRect.x = width
        self.libelle_plantRect.y = 400

        self.libelle_enlever = self.font.render("|ENLEVER|", True, WHITE, BLACK)
        self.libelle_enleverRect = self.libelle_enlever.get_rect()
        self.libelle_enleverRect.x = width
        self.libelle_enleverRect.y = 440

        self.libelle_planter = self.font.render("|PLANTER|", True, WHITE, BLACK)
        self.libelle_planterRect = self.libelle_planter.get_rect()
        self.libelle_planterRect.x = width
        self.libelle_planterRect.y = 480

        self.libelle_rabaisser = self.font.render("|RABAISSER|", True, WHITE, BLACK)
        self.libelle_rabaisserRect = self.libelle_rabaisser.get_rect()
        self.libelle_rabaisserRect.x = width
        self.libelle_rabaisserRect.y = 520

        self.libelle_monter = self.font.render("|MONTER|", True, WHITE, BLACK)
        self.libelle_monterRect = self.libelle_monter.get_rect()
        self.libelle_monterRect.x = width
        self.libelle_monterRect.y = 560

        self.libelle_aroser = self.font.render("|ARROSER|", True, WHITE, BLACK)
        self.libelle_aroserRect = self.libelle_aroser.get_rect()
        self.libelle_aroserRect.x = width
        self.libelle_aroserRect.y = 620

        self.libelle_engrais = self.font.render("|ENGRAIS|", True, WHITE, BLACK)
        self.libelle_engraisRect = self.libelle_engrais.get_rect()
        self.libelle_engraisRect.x = width
        self.libelle_engraisRect.y = 660

        self.libelle_piquet = self.font.render("travaux piquet", True, WHITE, BLACK)
        self.libelle_piquetRect = self.libelle_piquet.get_rect()
        self.libelle_piquetRect.x = width
        self.libelle_piquetRect.y = 740

        self.libelle_remplacer = self.font.render("|REMPLACER|", True, WHITE, BLACK)
        self.libelle_remplacerRect = self.libelle_remplacer.get_rect()
        self.libelle_remplacerRect.x = width
        self.libelle_remplacerRect.y = 780

        



        #############################################
        #############################################
        # format(self.parcel.largeur_rang, '.2f')
        self.libelle_largeur_rang = self.font.render("largeur rang  : " + str( self.parcel.largeur_rang) + "M" , True, WHITE, BLACK)
        self.libelle_largeur_rangRect = self.libelle_largeur_rang.get_rect() #font.render(format(zoom, '.2f')
        self.libelle_largeur_rangRect.x = 10
        self.libelle_largeur_rangRect.y = 400

        # format(self.parcel.distance_souche, '.2f')
        self.libelle_distance_cep = self.font.render("distance cep  : "+ str(self.parcel.distance_souche) +"M", True, WHITE, BLACK)
        self.libelle_distance_cepRect = self.libelle_distance_cep.get_rect()
        self.libelle_distance_cepRect.x = 10
        self.libelle_distance_cepRect.y = 440

        self.libelle_cepage = self.font.render("cepage  : "+ self.parcel.cepage , True, WHITE, BLACK)
        self.libelle_cepageRect = self.libelle_cepage.get_rect()
        self.libelle_cepageRect.x = 10
        self.libelle_cepageRect.y = 480

        self.libelle_nb_range = self.font.render("NB Rangé : " + str(len(self.parcel.vigne)), True, WHITE, BLACK)
        self.libelle_nb_rangeRect = self.libelle_nb_range.get_rect()
        self.libelle_nb_rangeRect.x = 20
        self.libelle_nb_rangeRect.y = 520

        self.libelle_nb_event = self.font.render("NB evenement : " + str(len(self.parcel.evenement)), True, WHITE, BLACK)
        self.libelle_nb_eventRect = self.libelle_nb_event.get_rect()
        self.libelle_nb_eventRect.x = 20
        self.libelle_nb_eventRect.y = 560


        self.update()







    def update(self):
        self.screen.blit(self.libelle_general, self.libelle_generalRect)
        self.screen.blit(self.buton_arbre, self.buton_arbreRect)
        self.screen.blit(self.buton_racine, self.buton_racineRect)
        self.screen.blit(self.buton_mort, self.buton_mortRect)
        self.screen.blit(self.buton_americain, self.buton_americainRect)
        self.screen.blit(self.buton_espalier, self.buton_espalierRect)
        self.screen.blit(self.buton_pulve, self.buton_pulveRect)
        self.screen.blit(self.buton_rabassier, self.buton_rabassierRect)
        self.screen.blit(self.libelle_plant, self.libelle_plantRect)
        self.screen.blit(self.libelle_piquet, self.libelle_piquetRect)
        self.screen.blit(self.libelle_enlever, self.libelle_enleverRect)
        self.screen.blit(self.libelle_planter, self.libelle_planterRect)
        self.screen.blit(self.libelle_rabaisser, self.libelle_rabaisserRect)
        self.screen.blit(self.libelle_monter, self.libelle_monterRect)
        self.screen.blit(self.libelle_aroser, self.libelle_aroserRect)
        self.screen.blit(self.libelle_engrais, self.libelle_engraisRect)
        self.screen.blit(self.libelle_remplacer, self.libelle_remplacerRect)
        self.nb_arbre = self.font.render(str(self.arbre), True, couleur_arbre, BLACK)
        self.screen.blit(self.nb_arbre, self.nb_arbreRect)
        self.nb_racine = self.font.render(str(self.racine), True, couleur_racine, BLACK)
        self.screen.blit(self.nb_racine, self.nb_racineRect)
        self.nb_mort = self.font.render(str(self.mort), True, couleur_mort, BLACK)
        self.screen.blit(self.nb_mort, self.nb_mortRect)
        self.nb_americain = self.font.render(str(self.americain), True, couleur_americain, BLACK)
        self.screen.blit(self.nb_americain, self.nb_americainRect)
        self.nb_espalier = self.font.render(str(self.espalier), True, couleur_espalier, BLACK)
        self.screen.blit(self.nb_espalier, self.nb_espalierRect)
        self.nb_pulve = self.font.render(str(self.pulve), True, couleur_pulve, BLACK)
        self.screen.blit(self.nb_pulve, self.nb_pulveRect)
        self.nb_rabassier = self.font.render(str(self.rabassier), True, couleur_rabassier, BLACK)
        self.screen.blit(self.nb_rabassier, self.nb_rabassierRect)
        

        #####################################
        #####################################
        if self.flag_info:
            l_r = float(self.parcel.largeur_rang)
            self.libelle_largeur_rang = self.font.render("largeur rang  : " + format( l_r, '.2f') + "M" , True, WHITE, BLACK)
            self.screen.blit(self.libelle_largeur_rang, self.libelle_largeur_rangRect)
            d_t = float(self.parcel.distance_souche)
            self.libelle_distance_cep = self.font.render("distance cep  : "+ format( d_t, '.2f') +"M", True, WHITE, BLACK)
            self.screen.blit(self.libelle_distance_cep , self.libelle_distance_cepRect )
            self.libelle_cepage = self.font.render("cepage  : "+ self.parcel.cepage , True, WHITE, BLACK)
            self.screen.blit(self.libelle_cepage , self.libelle_cepageRect )
            self.libelle_nb_range = self.font.render("NB Rangé : " + str(len(self.parcel.vigne)), True, WHITE, BLACK)
            self.screen.blit(self.libelle_nb_range , self.libelle_nb_rangeRect )
            self.libelle_nb_event = self.font.render("NB evenement : " + str(len(self.parcel.evenement)), True, WHITE, BLACK)
            self.screen.blit(self.libelle_nb_event , self.libelle_nb_eventRect )    

    def count_evenement(self):
        self.arbre = 0
        self.racine = 0
        self.mort = 0
        self.americain = 0
        self.espalier = 0
        self.pulve = 0
        self.rabassier = 0
        for ev in self.parcel.evenement:
            if ev[1] == "ARBRE":
                self.arbre += 1
            elif ev[1] == "RACINE":
                self.racine += 1
            elif ev[1] == "MORT":
                self.mort += 1
            elif ev[1] == "AMERICAIN":
                self.americain += 1
            elif ev[1] == "ESPALIER":
                self.espalier += 1
            elif ev[1] == "PULVE":
                self.pulve += 1
            elif ev[1] == "RABASSIER":
                self.rabassier += 1


    def gestion(self):
        while True:
            titre = "**EasyVine VIEW**   lat: " + format(self.latitude, '.7f') + "   long: " + format(self.longitude, '.7f') + "  track: " + format(self.track,'.2f') + "  altitude: " + format(self.altitude, '.4f')
            pygame.display.set_caption(titre) 
            pygame.Surface.fill(self.screen, BLACK)
            # c'est ici que je vais affficher les parcelle et les rang

            ################################### AFFICHER LA POSITION ACTUELLE ROND ROUGE  ############################################
            pygame.draw.circle(self.screen, RED, self.position_py, 8)  # long_pyg , lat_pyg

            ################################### AFFICHER LES POINTS GPS TOUR DE LA PARCELLE ###########################################
            for lon_lat in self.tour_parcelle_pyg:
                long_pyg, lat_pyg = lon_lat
                pygame.draw.circle(self.screen, YELLOW, (long_pyg, lat_pyg), 4)  # long_pyg , lat_pyg

            ################################## AFFICHER LES LIGNES QUI RELIES LES POINT GPS DU TOUR DE LA PARCELLE ###################
            if len(self.tour_parcelle_pyg) > 1:
                pygame.draw.lines(self.screen, YELLOW, True, self.tour_parcelle_pyg, 3)

            #################################  AFFICHER LES POINTS QUI COMPOSE LES RANGS   #############################
            if len(self.parcel.vigne) > 0: # il y a au moins un debut de rang
                for rang_py in self.vigne_pyg:
                    for lon_lat in rang_py:
                        long_pyg, lat_pyg = lon_lat
                        pygame.draw.circle(self.screen, GREEN, (long_pyg, lat_pyg), 4)  # long_pyg , lat_pyg
                    if len(rang_py) > 1:
                        pygame.draw.lines(self.screen, GREEN, True, rang_py, 3)

            ############################ AFFICHER LES EVENEMENTS #######################################
            # 
            if len(self.evenement_pyg) > 0:
                for evenement in self.evenement_pyg:
                    lon_lat, nom = evenement
                    long_pyg, lat_pyg = lon_lat
                    if nom == "ARBRE":
                        couleur = couleur_arbre
                    elif nom == "RACINE":
                        couleur = couleur_racine   
                    elif nom == "MORT":
                        couleur = couleur_mort
                    elif nom == "AMERICAIN":
                        couleur = couleur_americain
                    elif nom == "ESPALIER":
                        couleur = couleur_espalier
                    elif nom == "PULVE":
                        couleur = couleur_pulve
                    elif nom == "RABASSIER":
                        couleur = couleur_rabassier 

                    pygame.draw.circle(self.screen, couleur, (long_pyg, lat_pyg), 8)  # long_pyg , lat_pyg
                    

                        


            ########################################### AFFICHE LES MENUS ##############################
            self.window_main.update()  # # affiche a l'ecran les texte
            self.update()
            pygame.display.update()


            ####################################### PRENDRE LA POSITION ACTUELLE A L'ANGLE DE LA PARCELLE
            if len(self.parcel.tour) > 0: # le tour de la parcelle est existant est mode VIEW
                self.position_gps = self.parcel.tour[0] # on simule que le gps est au premier point de la parcelle
                self.track = 0 #  nord

            


            ###################### TRANSFORMER LES COORDONNEES GPS EN COORDONNE PYG ##############################
            if len(self.parcel.tour) > 0: # la parcelle a un tour donc transformer en pyg
                self.tour_parcelle_pyg, un_point_pyg, echelle, self.position_py = pyg.tour_parcelle(self.parcel.tour,
                                                                                                self.position_gps,
                                                                                                self.position_gps,
                                                                                                self.window_main.zoom, self.window_main.centre_x,
                                                                                                self.window_main.centre_y,
                                                                                                self.track)
            else:
                self.tour_parcelle_pyg = []

            if len(self.parcel.vigne) > 0: # il y a au moins un debut de rang
                self.vigne_pyg, self.tour_parcelle_pyg, self.position_py = pyg.rang_vigne_en_pyg(self.parcel.vigne,
                                                                                                self.parcel.tour,
                                                                                                self.position_gps,
                                                                                                self.window_main.zoom, self.window_main.centre_x,
                                                                                                self.window_main.centre_y,
                                                                                                 self.track)
            else:
                self.vigne_pyg = []

            if len(self.parcel.evenement) > 0:
                self.evenement_pyg, self.tour_parcelle_pyg, self.position_py = pyg.evenement_en_pyg(self.parcel.evenement,
                                                                                                    self.parcel.tour,
                                                                                                    self.position_gps,
                                                                                                    self.window_main.zoom, self.window_main.centre_x,
                                                                                                    self.window_main.centre_y,
                                                                                                    self.track)
            else:
                self.evenement_pyg = []
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window_main.index_action = -99 # permet de fermer le programe
                    
                    return 0  # return windowscan
                elif event.type == pygame.MOUSEBUTTONDOWN:


                    ###########################################################
                    ########## GERE LES EVENEMENTS DE LA window.main ##########
                    ###########################################################
                    ########## flag_info
                    if self.window_main.buton_infoRect.collidepoint(event.pos):
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

                        self.count_evenement()

                    elif self.window_main.bouton_parcelle_dRect.collidepoint(event.pos):  # change de parcelle
                        #self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.evenement_pyg = []
                        self.window_main.inc_index_parcelle()
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet

                        self.count_evenement()
                        


                    retour = self.window_main.gest_event(event, self.parcel)
                    if retour == 0 : # si l'ACTION change return a windowscan et return a main.py 
                        return 0