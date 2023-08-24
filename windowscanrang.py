


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

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



class WindowScanRang:
    def __init__(self, window_m, module, parcel):

        self.window_main = window_m
        self.screen = self.window_main.screen
        self.module = module
        self.parcel = parcel
        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_mg = pygame.font.Font('freesansbold.ttf', 50)
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

        self.list_undo = []

        self.a_arroser = False

        self.buton_state = GPIO.HIGH
        

        self.list_scan_quoi = ["DEBUT RANG", "FIN RANG", "PLANT", "PIQUET"]
        self.index_list_scan_quoi = 0
        self.scan_quoi = self.list_scan_quoi[self.index_list_scan_quoi]  # | AMMARE par default

        self.list_travaux_plant = ["AUCUN", "ENLEVER", "PLANTER", "RABAISSER", "MONTER"]  # liste des travaux a effectuer sur ce quoi SOUCHE
        self.index_travaux_plant = 0

        self.list_travaux_piquet = ["AUCUN", "REMPLACER"]  # liste des travaux a effectuer sur ce quoi
        self.index_travaux_piquet = 0

        self.buton_scan_quoi_g = self.font.render("<< :", True, config.YELLOW, config.GRAY)
        self.buton_scan_quoi_gRect = self.buton_scan_quoi_g.get_rect()
        self.buton_scan_quoi_gRect.x = 10
        self.buton_scan_quoi_gRect.y = 60

        self.buton_scan_quoi_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.buton_scan_quoi_dRect = self.buton_scan_quoi_d.get_rect()
        self.buton_scan_quoi_dRect.x = 285
        self.buton_scan_quoi_dRect.y = 60

        self.text_scan_quoi = self.font.render(self.list_scan_quoi[self.index_list_scan_quoi], True, config.GREEN, config.BLUE)
        self.text_scan_quoi_Rect = self.text_scan_quoi.get_rect()
        self.text_scan_quoi_Rect.x = 70
        self.text_scan_quoi_Rect.y = 60

        self.buton_scan= self.font_mg.render("| CLICK FOR SCAN |", True, config.YELLOW, config.GRAY)
        self.buton_scanRect = self.buton_scan.get_rect()
        self.buton_scanRect.x = 490
        self.buton_scanRect.y = 160

        self.text_libelle_travaux= self.font.render("TRAVAIL->", True, config.WHITE, config.BLACK)
        self.text_libelle_travauxRect = self.text_libelle_travaux.get_rect()
        self.text_libelle_travauxRect.x = 30
        self.text_libelle_travauxRect.y = 120

        self.buton_travaux_g = self.font.render("<< :", True, config.YELLOW, config.GRAY)
        self.buton_travaux_gRect = self.buton_travaux_g.get_rect()
        self.buton_travaux_gRect.x = 285
        self.buton_travaux_gRect.y = 120

        self.buton_travaux_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.buton_travaux_dRect = self.buton_travaux_d.get_rect()
        self.buton_travaux_dRect.x = 520
        self.buton_travaux_dRect.y = 120

        self.text_travaux= self.font.render(self.list_travaux_piquet[self.index_travaux_piquet],True , config.GREEN, config.BLUE)
        self.text_travauxRect = self.text_travaux.get_rect()
        self.text_travauxRect.x = 360
        self.text_travauxRect.y = 120

        self.buton_arroser = self.font_mg.render("A ARROSER", True, config.YELLOW, config.GRAY )
        self.buton_arroserRect = self.buton_arroser.get_rect()
        self.buton_arroserRect.x = 360
        self.buton_arroserRect.y = 60

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
        self.libelle_nb_rangeRect.x = 10
        self.libelle_nb_rangeRect.y = 520


        self.update()

    def update(self):
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


        self.screen.blit(self.buton_scan_quoi_g, self.buton_scan_quoi_gRect)
        self.screen.blit(self.buton_scan_quoi_d, self.buton_scan_quoi_dRect)
        self.text_scan_quoi = self.font.render(self.list_scan_quoi[self.index_list_scan_quoi], True, config.GREEN, config.BLUE)
        self.screen.blit(self.text_scan_quoi, self.text_scan_quoi_Rect)
        self.screen.blit(self.buton_scan, self.buton_scanRect)
        self.screen.blit(self.text_libelle_travaux, self.text_libelle_travauxRect)
        self.screen.blit(self.buton_travaux_g, self.buton_travaux_gRect)
        self.screen.blit(self.buton_travaux_d, self.buton_travaux_dRect)
        if self.a_arroser:
            self.buton_arroser = self.font_mg.render("A ARROSER", True, config.YELLOW, config.RED )
        else:
            self.buton_arroser = self.font_mg.render("A ARROSER", True, config.YELLOW, config.GRAY )
        self.screen.blit(self.buton_arroser, self.buton_arroserRect)        

        if self.index_list_scan_quoi == 2:# on scanne la souche
            self.text_travaux= self.font.render(self.list_travaux_plant[self.index_travaux_plant], True, config.GREEN, config.BLUE)
        else:
            self.text_travaux= self.font.render(self.list_travaux_piquet[self.index_travaux_piquet], True, config.GREEN, config.BLUE)
        self.screen.blit(self.text_travaux, self.text_travauxRect)


        
    def dec_scan_quoi(self):
        self.index_list_scan_quoi -= 1
        if self.index_list_scan_quoi == -1:
            self.index_list_scan_quoi = len(self.list_scan_quoi) - 1
        if self.index_list_scan_quoi != 2: # ce n'est pas un plant
            self.a_arroser = False 

    def inc_scan_quoi(self):
        self.index_list_scan_quoi += 1
        if self.index_list_scan_quoi == len(self.list_scan_quoi):
            self.index_list_scan_quoi = 0
        if self.index_list_scan_quoi != 2: # ce n'est pas un plant
            self.a_arroser = False

    def inc_travaux(self):
        if self.index_list_scan_quoi == 2: #on scanne les plant
            self.index_travaux_plant += 1
            if self.index_travaux_plant == len(self.list_travaux_plant):
                self.index_travaux_plant = 0
        else: # on scane les debut fin donc ammare et piquet
            self.index_travaux_piquet += 1
            if self.index_travaux_piquet == len(self.list_travaux_piquet):
                self.index_travaux_piquet = 0                 

    def dec_travaux(self):
        if self.index_list_scan_quoi == 2: #on scanne les plant
            self.index_travaux_plant -= 1
            if self.index_travaux_plant == -1:
                self.index_travaux_plant = len(self.list_travaux_plant) -1
        else: # on scane les debut fin donc ammare et piquet
            self.index_travaux_piquet -= 1
            if self.index_travaux_piquet == -1:
                self.index_travaux_piquet = len(self.list_travaux_piquet) - 1  


    def gestion(self):
        gs = main.GpsPoller()
        gs.start() # start it up

        buton = 4  #  c'est le bouton qui est sur le manche a droite et qui permet de scanner les rangs
        GPIO.setup(buton, GPIO.IN, GPIO.PUD_UP)
        self.buton_state = GPIO.HIGH

        erreurio = 0
        



        while True: # boucle principale

            
            titre = "**EasyVine SCAN RANG**   lat: " + format(self.latitude, '.7f') + "   long: " + format(self.longitude, '.7f') + "  track: " + format(self.track,'.2f') + "  altitude: " + format(self.altitude, '.4f')
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





            ################## afficher le niveau ################
            # pygame.draw.lines(screen, GRAY, True, [(deb_x, deb_y), (fin_x, deb_y), (fin_x, fin_y), (deb_x, fin_y)], 10)
            pygame.draw.lines(self.screen, config.GRAY, True, [(840, 10), (980, 10), (980, 150), (840, 150)], 5)
            pygame.draw.line(self.screen, config.GRAY, (910, 10), (910, 150), 4)
            pygame.draw.line(self.screen, config.GRAY, (840, 80), (980, 80), 4)
            pygame.draw.circle(self.screen, config.RED, (911 + self.roll * 5, 81 + self.pitch * 5), 10)  # long_pyg , lat_pyg

            ########################################### AFFICHE LES MENUS ##############################
            self.window_main.update()  # # affiche a l'ecran les texte
            self.module.update()
            self.update()
            pygame.display.update()

            ######################################################################
            ###############   CALCULER LES RANGS   ############################
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

            if  self.buton_state == GPIO.HIGH:         # c'est que l'on n a pas appyuyer sur CLICK FOR SCANNE
                self.buton_state = GPIO.input(buton)  # donc on vas chercher l'etat du bouton de la poignet
            if self.buton_state == GPIO.LOW: # ici on a appuyé sur le bouton de la poignet  ou sur le bouton CLICK FOR SCANNE

                ######################  SCANNE LES RANGS     ######################
                self.buton_state = GPIO.HIGH # sinon on rentre dans une boucle infini ou button_state = GPIO.LOW
                ######################  SCANNE LES DEBUTS DE RANGS     ######################
                if self.index_list_scan_quoi == 0: # on scanne les debut de rang donc ammare
                    self.parcel.position = [self.position_gps, "AMMARE", "2023", self.altitude_gps, self.a_arroser, self.list_travaux_piquet[self.index_travaux_piquet]]
                    operation_ok , self.parcel.vigne =  add_debut_rang_in_list_rang(self.parcel.position, self.parcel.vigne, float(self.parcel.largeur_rang ))
                    if operation_ok:
                        self.list_undo.append(self.parcel.position)
                    else:    
                        print("LE DEBUT DE RANG N'A PAS ETE AJOUTER CAR IL EST TROPS PROCHE D'UNE AUTRE DEBUT DE RANG")

                ######################  SCANNE LES FINS DE RANGS     ######################
                elif self.index_list_scan_quoi == 1: # on scanne les fin de rang donc ammare
                    self.parcel.position = [self.position_gps, "AMMARE", "2023", self.altitude_gps, self.a_arroser, self.list_travaux_piquet[self.index_travaux_piquet]]
                    operation_ok , self.parcel.vigne =  add_fin_rang_in_list_rang(self.parcel.position, self.parcel.vigne, float(self.parcel.largeur_rang ))
                    if operation_ok:
                        self.list_undo.append(self.parcel.position)
                    else:    
                        print("LE fin DE RANG N'A PAS ETE AJOUTER CAR IL EST TROPS PROCHE D'UNE AUTRE fin DE RANG")
                elif self.index_list_scan_quoi == 2: # on scanne les plant
                    print("plant")
                elif self.index_list_scan_quoi == 3: # on scanne les piquet
                    print("piquet")



            if len(self.parcel.vigne) > 0: # il y a au moins un debut de rang
                self.vigne_pyg, self.tour_parcelle_pyg, self.position_py = pyg.rang_vigne_en_pyg(self.parcel.vigne,
                                                                                                self.parcel.tour,
                                                                                                self.position_gps,
                                                                                                self.window_main.zoom, self.window_main.centre_x,
                                                                                                self.window_main.centre_y,
                                                                                                 self.track)


            self.tour_parcelle_pyg, un_point_pyg, echelle, self.position_py = pyg.tour_parcelle(self.parcel.tour,
                                                                                                self.position_gps,
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
                    if self.buton_scan_quoi_gRect.collidepoint(event.pos):
                        self.dec_scan_quoi()
                    elif self.buton_scan_quoi_dRect.collidepoint(event.pos):
                        self.inc_scan_quoi()
                    
                    elif self.buton_travaux_dRect.collidepoint(event.pos):
                        self.inc_travaux()
                    elif self.buton_travaux_gRect.collidepoint(event.pos):
                        self.dec_travaux()    
                    
                    elif self.buton_arroserRect.collidepoint(event.pos):
                        if self.index_list_scan_quoi == 2: # on scanne les plants donc on peu les arroser
                            if self.a_arroser:
                                self.a_arroser = False
                            else:
                                self.a_arroser = True 

                    elif self.buton_scanRect.collidepoint(event.pos): # on vien de clicker sur CLICK FOR SCAN
                        self.buton_state = GPIO.LOW




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
                        self.windowalerte = windowalerte.WindowAlerte(self.screen, "voulez vous detruire la vigne de ",self.window_main.name_parcelle)  # creer la fenetre d'alerte
                        print("MODULE A IMPLEMENTER")
                        if self.windowalerte.update():  # attente de reponse de la fenetre d'alerte
                            
                            self.parcel.vigne = []
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
                        self.window_main.dec_index_parcelle()
                        
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet
                        
                    elif self.window_main.bouton_parcelle_dRect.collidepoint(event.pos):  # change de parcelle
                        #self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.window_main.inc_index_parcelle()
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet

                    retour = self.window_main.gest_event(event, self.parcel)
                    if retour == 0 : # si l'ACTION change return a windowscan et return a main.py 
                        return 0


