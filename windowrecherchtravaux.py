# windowrecherchtravaux






TIME_MSG = 1
import config
import main
import routine_gps
import windowalerte
import pyg
from communication import*
from routine_vigne import*

import time
import pygame
pygame.init()




import sys




class WindowRecherchTravaux:
    def __init__(self, window_m, module, parcel):

        print ("JE CREER L OBJET ")
        print ("JE CREER L OBJET ")

        self.window_main = window_m
        self.screen = self.window_main.screen
        self.module = module
        self.parcel = parcel
        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_mg = pygame.font.Font('freesansbold.ttf', 50)
        self.font_g = pygame.font.Font('freesansbold.ttf', 80)


        self.libelle_general = self.font_g.render("TRAVAUX ROUTINE NON IMPLANTE", True, config.WHITE, config.BLACK)
        self.libelle_generalRect = self.libelle_general.get_rect()
        self.libelle_generalRect.x = 10
        self.libelle_generalRect.y = 200

        self.flag_info = False

        self.libelle_saving = self.font_g.render("** SAVING **", True, config.GREEN, config.GRAY)
        self.libelle_savingRect = self.libelle_saving.get_rect()
        self.libelle_savingRect.x = 400
        self.libelle_savingRect.y = 400

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

        self.list_undo = []

       




        self.evenement_signale = False

        
       

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
        self.screen.blit(self.libelle_general, self.libelle_generalRect)

        

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




    def gestion(self):########### EVENEMENT #########
        gs = main.GpsPoller()
        gs.start() # start it up



        erreurio = 0







        while True:
            titre = "**EasyVine RECHERCHE TRAVAUX **   lat: " + format(self.latitude, '.7f') + "   long: " + format(self.longitude, '.7f') + "  track: " + format(self.track,'.2f') + "  altitude: " + format(self.altitude, '.4f')
            pygame.display.set_caption(titre) 
            pygame.Surface.fill(self.screen, config.BLACK)
            # c'est ici que je vais affficher les parcelle et les rang

 
                        


            ########################################### AFFICHE LES MENUS ##############################
            self.window_main.update()  # # affiche a l'ecran les texte
            self.module.update()
            self.update()
            pygame.display.update()




            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.windowalerte = windowalerte.WindowAlerte(self.screen, "voulez vous sauvegarder la vigne ","de la parcelle")  # creer la fenetre d'alerte
                    if self.windowalerte.update():  # attente de reponse de la fenetre d'alerte
                        self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                    self.window_main.index_action = -99 # permet de fermer le programe
                    gs.running = False
                    gs.join() # wait for the thread to finish what it's doing
                    del(gs)
                    return 0  # return windowscan
                
                elif event.type == pygame.MOUSEBUTTONDOWN:

                   
                    

                    ########## ON RETURN AU FICHIER windowscan POUR CHANGER DE MODULE ###########
                    if self.module.buton_gRect.collidepoint(event.pos):
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


                