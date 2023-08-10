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



    def gestion(self):
        while True:
            titre = "**EasyVine SCAN EVENEMENT **   lat: " + str(self.latitude) + "   long: " + str(self.longitude) + "  track: " + str(self.track) + "  altitude: " + str(self.altitude)
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
                        
                    elif self.window_main.bouton_parcelle_dRect.collidepoint(event.pos):  # change de parcelle
                        #self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.evenement_pyg = []
                        self.window_main.inc_index_parcelle()
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet

                    retour = self.window_main.gest_event(event, self.parcel)
                    if retour == 0 : # si l'ACTION change return a windowscan et return a main.py 
                        return 0