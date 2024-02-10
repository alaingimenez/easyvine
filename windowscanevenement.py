


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




class WindowScanEvenement:
    def __init__(self, window_m, module, parcel):

        self.window_main = window_m
        self.screen = self.window_main.screen
        self.module = module
        self.parcel = parcel
        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_mg = pygame.font.Font('freesansbold.ttf', 90)
        self.font_g = pygame.font.Font('freesansbold.ttf', 80)

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

        self.buton_state = 1




        self.evenement_signale = False

        width = 600 + 500
        index_decalage = 110
        decalage = 0
        self.buton_arbre = self.font_mg.render("|ARBRE|", True, config.couleur_arbre, config.GRAY)
        self.buton_arbreRect = self.buton_arbre.get_rect()
        self.buton_arbreRect.x = width
        self.buton_arbreRect.y = 60 + decalage
        decalage += index_decalage

        self.buton_racine = self.font_mg.render("|RACINE|", True, config.couleur_racine, config.GRAY)
        self.buton_racineRect = self.buton_racine.get_rect()
        self.buton_racineRect.x = width
        self.buton_racineRect.y = 60 + decalage
        decalage += index_decalage

        self.buton_mort = self.font_mg.render("|MORT|", True, config.couleur_mort, config.GRAY)
        self.buton_mortRect = self.buton_mort.get_rect()
        self.buton_mortRect.x = width
        self.buton_mortRect.y = 60 + decalage
        decalage += index_decalage

        self.buton_americain = self.font_mg.render("|AMERICAIN|", True, config.couleur_americain, config.GRAY)
        self.buton_americainRect = self.buton_americain.get_rect()
        self.buton_americainRect.x = width
        self.buton_americainRect.y = 60 + decalage
        decalage += index_decalage

        self.buton_espalier = self.font_mg.render("|ESPALIER|", True, config.couleur_espalier, config.GRAY)
        self.buton_espalierRect = self.buton_espalier.get_rect()
        self.buton_espalierRect.x = width
        self.buton_espalierRect.y = 60 + decalage
        decalage += index_decalage

        self.buton_pulve = self.font_mg.render("|PULVE|", True, config.couleur_pulve, config.GRAY)
        self.buton_pulveRect = self.buton_pulve.get_rect()
        self.buton_pulveRect.x = width
        self.buton_pulveRect.y = 60 + decalage
        decalage += index_decalage

        self.buton_rabassier = self.font_mg.render("|RABASSIER|", True, config.couleur_rabassier, config.GRAY)
        self.buton_rabassierRect = self.buton_rabassier.get_rect()
        self.buton_rabassierRect.x = width
        self.buton_rabassierRect.y = 60 + decalage
        

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

        #buton = 4  #  c'est le bouton qui est sur le manche a droite et qui permet de scanner les rangs
        #GPIO.setup(buton, GPIO.IN, GPIO.PUD_UP)
        self.buton_state = 1

        erreurio = 0







        while True:
            titre = "**EasyVine SCAN EVENEMENT **   lat: " + format(self.latitude, '.7f') + "   long: " + format(self.longitude, '.7f') + "  track: " + format(self.track,'.2f') + "  altitude: " + format(self.altitude, '.4f')
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

            ######################################################################
            ###############   CALCULER ET SCANNER LES EVENEMENT   ################
            ######################################################################
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

            if  self.buton_state == 1:         # c'est que l'on n a pas appyuyer sur CLICK FOR SCANNE
                if config.BUTON_SCAN.is_pressed:      # donc on vas chercher l'etat du bouton de la poignet
                    self.buton_state = 0 
            if self.buton_state == 0: # ici on a appuyé sur le bouton de la poignet  ou sur le bouton CLICK FOR SCANNE
                # ici on peut faire un action si l'on appuy sur le bouton poignet
                self.buton_state = 1 # sinon on rentre dans une boucle infini ou button_state = GPIO.LOW

            ########################## C'EST ICI QUE L'ON VA RENTRER LES EVENEMENTS #############
            if self.evenement_signale: # un evenement a ete signalé donc l'ajouter a la liste
                self.evenement_signale = False
                print(self.parcel.name_evenement)
                self.parcel.position_evenement = [(self.latitude, self.longitude),self.parcel.name_evenement]
                self.parcel.evenement.append(self.parcel.position_evenement)








            ###################### TRANSFORMER LES COORDONNEES GPS EN COORDONNE PYG ##############################
            if len(self.parcel.vigne) > 0: # il y a au moins un debut de rang
                self.vigne_pyg, self.tour_parcelle_pyg, self.position_py = pyg.rang_vigne_en_pyg(self.parcel.vigne,
                                                                                                self.parcel.tour,
                                                                                                self.position_gps,
                                                                                                self.window_main.zoom, self.window_main.centre_x,
                                                                                                self.window_main.centre_y,
                                                                                                 self.track)
            if len(self.parcel.evenement) > 0:
                self.evenement_pyg, self.tour_parcelle_pyg, self.position_py = pyg.evenement_en_pyg(self.parcel.evenement,
                                                                                                    self.parcel.tour,
                                                                                                    self.position_gps,
                                                                                                    self.window_main.zoom, self.window_main.centre_x,
                                                                                                    self.window_main.centre_y,
                                                                                                    self.track)    




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
                    # ICI gerer les evenements de cette fenetre 
                    if self.buton_arbreRect.collidepoint(event.pos):
                        self.parcel.name_evenement = "ARBRE"
                        self.evenement_signale = True
                    elif self.buton_racineRect.collidepoint(event.pos):
                        self.parcel.name_evenement = "RACINE"
                        self.evenement_signale = True
                    elif self.buton_mortRect.collidepoint(event.pos):
                        self.parcel.name_evenement = "MORT"
                        self.evenement_signale = True
                    elif self.buton_americainRect.collidepoint(event.pos):
                        self.parcel.name_evenement = "AMERICAIN"
                        self.evenement_signale = True
                    elif self.buton_espalierRect.collidepoint(event.pos):
                        self.parcel.name_evenement = "ESPALIER"
                        self.evenement_signale = True
                    elif self.buton_pulveRect.collidepoint(event.pos):
                        self.parcel.name_evenement = "PULVE"
                        self.evenement_signale = True
                    elif self.buton_rabassierRect.collidepoint(event.pos):
                        self.parcel.name_evenement = "RABASSIER"
                        self.evenement_signale = True

                        




                    ##-----------------------------------------------------------
                    ##-----------------------------------------------------------
                    ########## GERE LES EVENEMENTS DE LA windowscan module
                    elif self.module.buton_undoRect.collidepoint(event.pos): # BUTON UNDO
                        print("MODULE A IMPLEMENTER")
                        if len(self.parcel.vigne) > 0:
                            pass
                            # self.list_undo.append(self.parcel.vigne.pop())
                    elif self.module.buton_redoRect.collidepoint(event.pos): # BUTON REDO
                        print("MODULE A IMPLEMENTER")
                        if len(self.list_undo) > 0:
                            pass
                            #self.parcel.vigne.append(self.list_undo.pop())
                    elif self.module.buton_delRect.collidepoint(event.pos):
                        print("MODULE A IMPLEMENTER")
                        self.windowalerte = windowalerte.WindowAlerte(self.screen, "voulez vous detruire tous les evenements ",self.window_main.name_parcelle)  # creer la fenetre d'alerte
                        if self.windowalerte.update():  # attente de reponse de la fenetre d'alerte
                            self.parcel.evenement = []
                            self.evenement_pyg = []
                            #self.list_undo.append(self.parcel.tour.pop())
                    elif self.module.buton_saveRect.collidepoint(event.pos):
                        print("id parcel :", id(self.parcel))
                        self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        print("id parcel :", id(self.parcel))
                        self.screen.blit(self.libelle_saving, self.libelle_savingRect)
                        pygame.display.update()
                        time.sleep(TIME_MSG)

                    

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


                