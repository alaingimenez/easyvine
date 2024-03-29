



TIME_MSG = 1

import config
import main
import routine_gps
import windowalerte
import pyg

import time
import pygame
pygame.init()









class WindowScanParcelle:
    def __init__(self, window_m, module, parcel):

        self.window_main = window_m
        self.screen = self.window_main.screen
        self.module = module
        self.parcel = parcel
        
        #print("id parcel :", id(self.parcel))
        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet
        #print("id parcel :", id(self.parcel))

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_g = pygame.font.Font('freesansbold.ttf', 80)

        self.flag_info = False

        
        self.latitude = 0
        self.longitude = 0
        self.pitch = 0
        self.roll = 0
        self.track = 0
        self.altitude = 0
        
        self.position_gps = (0, 0)
        self.track = 0
        self.position_py = (0,0)
        self.tour_parcelle_pyg =[]
        self.list_undo = []

        self.distance_point = 0.0 # quand on rentre un valeur le scan du tour de la parcelle devient automatique et chaque
                                  # et un point est rentré a chaque tronçon de cette valeur en metre  

        self.index_scan_mode = 0 #   = 0 mode VIEW  = 1 mode PAUSE   = 2 mode REC
        
        self.libelle_saving = self.font_g.render("** SAVING **", True, config.GREEN, config.GRAY)
        self.libelle_savingRect = self.libelle_saving.get_rect()
        self.libelle_savingRect.x = 400
        self.libelle_savingRect.y = 400
        

        self.buton_rec = self.font.render("|  REC  |", True, config.YELLOW, config.GRAY)
        self.buton_recRect = self.buton_rec.get_rect()
        self.buton_recRect.x = 350
        self.buton_recRect.y = 80

        self.buton_pause = self.font.render("|PAUSE|", True, config.YELLOW, config.GRAY)
        self.buton_pauseRect = self.buton_pause.get_rect()
        self.buton_pauseRect.x = 470
        self.buton_pauseRect.y = 80

        self.buton_view = self.font.render("|VIEW|", True, config.YELLOW, config.RED)
        self.buton_viewRect = self.buton_view.get_rect()
        self.buton_viewRect.x = 610
        self.buton_viewRect.y = 80

        self.libelle_distance = self.font.render("Distance Point", True, config.WHITE , config.BLACK)
        self.libelle_distanceRect = self.libelle_distance.get_rect()
        self.libelle_distanceRect.x = 30
        self.libelle_distanceRect.y = 50

        self.buton_distance_g = self.font.render("<< :", True, config.YELLOW, config.GRAY)
        self.buton_distance_gRect = self.buton_distance_g.get_rect()
        self.buton_distance_gRect.x = 33+20
        self.buton_distance_gRect.y = 80

        self.buton_distance_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.buton_distance_dRect = self.buton_distance_d.get_rect()
        self.buton_distance_dRect.x = 150+20
        self.buton_distance_dRect.y = 80

        self.text_distance = self.font.render(format(self.distance_point,'.2f'), True, config.GREEN, config.BLUE)
        self.text_distanceRect = self.text_distance.get_rect()
        self.text_distanceRect.x = 90+20
        self.text_distanceRect.y = 80

        ####################################################### consite a enlever des points pour gagner de la vitesse
        ### CI DESSOU LA SIMPLIFICATION DU TOUR DE PARCELLE ### a l'affichage
        #######################################################
        self.buton_simplifie = self.font.render("|SIMPLIFIE|", True, config.YELLOW, config.GRAY)
        self.buton_simplifieRect = self.buton_simplifie.get_rect()
        self.buton_simplifieRect.x = 975
        self.buton_simplifieRect.y = 10

        self.buton_simplifie_g = self.font.render("<< :", True, config.YELLOW, config.GRAY)
        self.buton_simplifie_gRect = self.buton_simplifie_g.get_rect()
        self.buton_simplifie_gRect.x = 930
        self.buton_simplifie_gRect.y = 65

        self.buton_simplifie_enleve = self.font.render("|ENLEVE|", True, config.YELLOW, config.GRAY)
        self.buton_simplifie_enleveRect = self.buton_simplifie_enleve.get_rect()
        self.buton_simplifie_enleveRect.x = 990
        self.buton_simplifie_enleveRect.y = 50

        self.buton_simplifie_remet = self.font.render("|REMET|", True, config.YELLOW, config.GRAY)
        self.buton_simplifie_remetRect = self.buton_simplifie_remet.get_rect()
        self.buton_simplifie_remetRect.x = 1000
        self.buton_simplifie_remetRect.y = 90

        self.buton_simplifie_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.buton_simplifie_dRect = self.buton_simplifie_d.get_rect()
        self.buton_simplifie_dRect.x = 1135
        self.buton_simplifie_dRect.y = 65

        self.mode_simplifie = False  # si = a True on peut simplifier le tour de la parcelle
        self.nb_point_tour_parcelle = len(self.tour_parcelle_pyg)-1
        self.point_vise = self.nb_point_tour_parcelle # c'est le point entoure de blanc qui pourrat etre detruit
        # ci dessou variable pour remetre le point
        self.pos_enleve = 0 # c'est la position dans la liste du point qui viens d'etre enleve
        self.lon_lat_enleve = (0,0) # ce sont les valeur du point qui vient d'etre enleve 
        self.remetre = False # il faut etre = a True pour remetre le point

        ################################################################################################
        ### CI DESSOU POUR FAIRE FONCTIONNER LE SCAN EN APPUYANT SUR LE BOUTON POUR RENTRER LE POINT ###
        ################################################################################################
        self.automatique_or_buton = True       # False scan est en mode automatique si True il faut appuyer le bouton
        self.text_automatique_or_buton = self.font.render(format("|BOUTON|"), True, config.YELLOW, config.GRAY)
        self.text_automatique_or_butonRect = self.text_automatique_or_buton.get_rect()
        self.text_automatique_or_butonRect.x = 50
        self.text_automatique_or_butonRect.y = 120

        self.buton_state = 1



        ############################################
        ### CI DESSOU LES INFOS PARCELLE ###
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

        self.screen.blit(self.buton_rec, self.buton_recRect)
        self.screen.blit(self.buton_pause, self.buton_pauseRect)
        self.screen.blit(self.buton_view,self.buton_viewRect)
        self.screen.blit(self.libelle_distance, self.libelle_distanceRect)
        self.screen.blit(self.buton_distance_g, self.buton_distance_gRect)
        self.screen.blit(self.buton_distance_d, self.buton_distance_dRect)
        self.text_distance = self.font.render(format(self.distance_point,'.2f'), True, config.GREEN, config.BLUE)
        self.screen.blit(self.text_distance, self.text_distanceRect)

        if self.automatique_or_buton:       # le scan est en mode automatique si True il faut appuyer le bouton
            self.text_automatique_or_buton = self.font.render(format("|BOUTON|"), True, config.YELLOW, config.GRAY)
        else:
            self.text_automatique_or_buton = self.font.render(format("AUTOMATIQUE"), True, config.GREEN, config.BLUE)
        self.screen.blit(self.text_automatique_or_buton, self.text_automatique_or_butonRect)

        if self.mode_simplifie:
            self.buton_simplifie = self.font.render("|SIMPLIFIE|", True, config.YELLOW, config.RED)
        else:
            self.buton_simplifie = self.font.render("|SIMPLIFIE|", True, config.YELLOW, config.GRAY)
        
        self.screen.blit(self.buton_simplifie, self.buton_simplifieRect)
        self.screen.blit(self.buton_simplifie_g, self.buton_simplifie_gRect)
        self.screen.blit(self.buton_simplifie_enleve, self.buton_simplifie_enleveRect)
        self.screen.blit(self.buton_simplifie_remet, self.buton_simplifie_remetRect)
        self.screen.blit(self.buton_simplifie_d, self.buton_simplifie_dRect)



    def scan_mode(self):
        if self.index_scan_mode == 0:  # mode VIEW
            self.buton_view = self.font.render("|VIEW|", True, config.YELLOW, config.RED)
            self.buton_pause = self.font.render("|PAUSE|", True, config.YELLOW, config.GRAY)
            self.buton_rec = self.font.render("|  REC  |", True, config.YELLOW, config.GRAY)
        elif self.index_scan_mode == 1: # mode PAUSE
            self.buton_view = self.font.render("|VIEW|", True, config.YELLOW, config.GRAY)
            self.buton_pause = self.font.render("|PAUSE|", True, config.YELLOW, config.RED)
            self.buton_rec = self.font.render("|  REC  |", True, config.YELLOW, config.GRAY)
        elif self.index_scan_mode == 2: # mode REC
            self.buton_view = self.font.render("|VIEW|", True, config.YELLOW, config.GRAY)
            self.buton_pause = self.font.render("|PAUSE|", True, config.YELLOW,config. GRAY)
            self.buton_rec = self.font.render("|  REC  |", True, config.YELLOW, config.RED)

    def dec_distance_point(self):
        self.distance_point -= 0.2
        self.distance_point = round(self.distance_point, 1)
        if self.distance_point <= 0:
            self.distance_point = 0
            self.automatique_or_buton = True # passage en mode bouton 


    def inc_distance_point(self):
        self.distance_point += 0.2
        self.automatique_or_buton = False       # le scan est en mode automatique

    def save_anciene_version_en_new(self):
        print(" je charge la parcelle : ", self.window_main.name_parcelle)
        list = self.window_main.fichier.ancien_V_parcel_load(self.window_main.name_parcelle)
        info_vigne, tours_parcelle = list
        self.parcel.largeur_rang, self.parcel.distance_souche, self.parcel.cepage = info_vigne
        self.parcel.tour = tours_parcelle

        self.affiche_parcelle()

        self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)

    def affiche_parcelle(self):
        print(self.window_main.name_parcelle)
        print(self.parcel.largeur_rang)
        print(self.parcel.distance_souche)
        print(self.parcel.cepage)
        print(self.parcel.tour)






    def gestion(self):
        gs = main.GpsPoller()
        gs.start() # start it up
        
        latitude = gs.gpsd.fix.latitude

        longitude = gs.gpsd.fix.longitude
        self.position_gps = (latitude, longitude)

        self.track = gs.gpsd.fix.track
        self.altitude = gs.gpsd.fix.altitude

        self.buton_state = 1
       

        while True:
            titre = "**EasyVine SCAN PARCELLE **   lat: " + format(latitude, '.7f') + "   long: " + format(longitude, '.7f') + "  track: " + format(self.track,'.2f')  # + "  altitude: " + format(self.altitude, '.4f')
            pygame.display.set_caption(titre)


            pygame.Surface.fill(self.screen, config.BLACK)
            # c'est ici que je vais affficher les parcelle et les rang

            ################################### AFFICHER LA POSITION ACTUELLE ROND ROUGE  ############################################
            pygame.draw.circle(self.screen, config.RED, self.position_py, 8)  # long_pyg , lat_pyg

            ########## si mode simplifie en cours entourer le point visé ######################
            if self.mode_simplifie:
                #print("popint vise = ", self.point_vise)
                lon_lat = self.tour_parcelle_pyg[self.point_vise]
                
                #print("lng tour parcelle", len(self.tour_parcelle_pyg))
                long_pyg, lat_pyg = lon_lat
                pygame.draw.circle(self.screen, config.WHITE, (long_pyg, lat_pyg), 12)  # long_pyg , lat_pyg 
            
            
            
            
            ################################### AFFICHER LES POINTS GPS TOUR DE LA PARCELLE ###########################################
            for lon_lat in self.tour_parcelle_pyg:
                long_pyg, lat_pyg = lon_lat
                pygame.draw.circle(self.screen, config.YELLOW, (long_pyg, lat_pyg), 4)  # long_pyg , lat_pyg

            ################################## AFFICHER LES LIGNES QUI RELIES LES POINT GPS DU TOUR DE LA PARCELLE ###################
            if len(self.tour_parcelle_pyg) > 1:
                if self.index_scan_mode == 0: # mode VIEW donc feme la parcelle
                    fermer = True
                else:
                    fermer = False
                pygame.draw.lines(self.screen, config.YELLOW, fermer, self.tour_parcelle_pyg, 3)



            ########################################### AFFICHE LES MENUS ##############################
            self.window_main.update()  # # affiche a l'ecran les texte
            self.module.update()
            self.update()
            pygame.display.update()

            ######################################################################
            ###############   CALCULER LA PARCELLE ############################
            ######################################################################
            
            latitude = gs.gpsd.fix.latitude
            longitude = gs.gpsd.fix.longitude
            self.position_gps = (latitude, longitude)

            self.track = gs.gpsd.fix.track
            #self.altitude = gpsd.fix.altitude
            
            """
            print(gs.lat) # = gpsd.fix.latitude
            longitude = gpsd.fix.longitude
            speed = gpsd.fix.speed
            altitude = gpsd.fix.altitude
            jourheure = gpsd.fix.time
            status =  gpsd.fix.status  #gpsd.fix.status  ou mode
            mode = gpsd.fix.mode
            track = gpsd.fix.track   # Degrees from true north
            climb = gpsd.fix.climb
            """
            # si la parcelle a un tour on le visualise sinon on est pret pour le scanner
            # il faudrat rajouter des bouton pour modifier une parcelle scanner
            if len(self.parcel.tour) > 0 and self.index_scan_mode == 0: # le tour de la parcelle est existant est mode VIEW
                self.position_gps = self.parcel.tour[0] # on simule que le gps est au premier point de la parcelle
                self.track = 0 #  nord

            # MODE REC
            if self.index_scan_mode == 2: # mode REC

                if self.automatique_or_buton: ### ON EST EN MODE BOUTON POUR RENTRER LES POINTS DE LA PARCELLE
                    if  self.buton_state == 1:         # c'est que l'on n a pas appyuyer sur BOUTON
                        if config.BUTON_SCAN.is_pressed:      # donc on vas chercher l'etat du bouton de la poignet
                            self.buton_state = 0        # car le bouton est pressé 

                    if self.buton_state == 0: # ici on a appuyé sur le bouton de la poignet  ou sur le bouton BOUTON
                        self.buton_state = 1 # sinon on rentre dans une boucle infini 
                        ### ICI RENTRE LE POINT DE LA PARCELLE 
                        if len(self.parcel.tour) == 0: # si la parcelle est vide
                            self.parcel.tour.append(self.position_gps) # ajouter la premiere position

                        last_position = self.parcel.tour[-1]
                        distance_last_position = routine_gps.get_distance_gps(last_position, self.position_gps)
                        if distance_last_position > 0.5: # empeche de rentrer des point a moins de 0.5 metre de distance si on laisse le bouton appuye
                            self.parcel.tour.append(self.position_gps)





                else: ### ON EST EN MODE AUTOMATIQUE les points rentre avec le deplacement et la distance point
                    if len(self.parcel.tour) == 0: # si la parcelle est vide
                        self.parcel.tour.append(self.position_gps) # ajouter la premiere position
                    last_position = self.parcel.tour[-1]
                    distance_last_position = routine_gps.get_distance_gps(last_position, self.position_gps)
                    if distance_last_position > self.distance_point:
                        self.parcel.tour.append(self.position_gps)




            self.tour_parcelle_pyg, un_point_pyg, echelle, self.position_py = pyg.tour_parcelle(self.parcel.tour,
                                                                                                self.position_gps,
                                                                                                self.position_gps,
                                                                                                self.window_main.zoom, self.window_main.centre_x,
                                                                                                self.window_main.centre_y,
                                                                                                self.track)




            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.windowalerte = windowalerte.WindowAlerte(self.screen, "voulez vous sauvegarder le tour ","de la parcelle")  # creer la fenetre d'alerte
                    if self.windowalerte.update():  # attente de reponse de la fenetre d'alerte
                        self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                    self.window_main.index_action = -99 # permet de fermer le programe
                    gs.running = False
                    gs.join() # wait for the thread to finish what it's doing
                    del(gs)
                    return 0  # return windowscan

                    

                elif event.type == pygame.MOUSEBUTTONDOWN:
                        ######### CHANGEMENT DE MODE DE SCAN   VIEW / PAUSE / REC
                    if self.buton_viewRect.collidepoint(event.pos):
                        self.index_scan_mode = 0  # VIEW
                        self.scan_mode()
                    elif self.buton_pauseRect.collidepoint(event.pos):
                        self.index_scan_mode = 1  # PAUSE
                        self.scan_mode()
                    elif self.buton_recRect.collidepoint(event.pos):
                        self.index_scan_mode = 2  # REC
                        self.scan_mode()

                    ### BOUTON DU MODE SIMPLIFIE ##
                    elif self.buton_simplifieRect.collidepoint(event.pos):
                        if self.mode_simplifie:
                            self.mode_simplifie = False
                        else:
                            self.mode_simplifie = True
                            self.nb_point_tour_parcelle = len(self.tour_parcelle_pyg)-1
                            self.point_vise = self.nb_point_tour_parcelle
                    elif self.buton_simplifie_dRect.collidepoint(event.pos) and self.mode_simplifie:
                        if self.point_vise == self.nb_point_tour_parcelle:
                            self.point_vise = 1
                        else:
                            self.point_vise += 1
                    elif self.buton_simplifie_gRect.collidepoint(event.pos) and self.mode_simplifie:
                        if self.point_vise == 1:
                            self.point_vise = self.nb_point_tour_parcelle
                        else:
                            self.point_vise -= 1 
                    elif self.buton_simplifie_enleveRect.collidepoint(event.pos) and self.mode_simplifie:
                        #detruire l'element vise
                        self.pos_enleve = self.point_vise
                        self.lon_lat_enleve = self.parcel.tour[self.point_vise]
                        self.remetre = True
                        del self.parcel.tour[self.point_vise]
                        self.nb_point_tour_parcelle -= 1
                        if self.point_vise > self.nb_point_tour_parcelle:
                            self.point_vise = self.nb_point_tour_parcelle
                    elif self.buton_simplifie_remetRect.collidepoint(event.pos)  and self.remetre:
                        print ("je remet le point")
                        self.remetre = False 
                        self.parcel.tour.insert(self.pos_enleve, self.lon_lat_enleve)
                    # fait comme si on appuy sur le bouton de la poignet au click BOUTON
                    # a condition que l'on soit en mode REC et BOUTON    
                    elif self.text_automatique_or_butonRect.collidepoint(event.pos) and self.automatique_or_buton and self.index_scan_mode == 2: # on vien de clicker sur CLICK FOR SCAN
                        self.buton_state = 0
                        
                        

                    ########### GESTION DE LA DISTANCE POINTS  #####################
                    elif self.buton_distance_gRect.collidepoint(event.pos):
                        self.dec_distance_point()
                    elif self.buton_distance_dRect.collidepoint(event.pos):
                        self.inc_distance_point()

                    ########### GESTION AFFICAHGE DES INFOS PARCELLE  #####################
                    elif self.window_main.buton_infoRect.collidepoint(event.pos):
                        if self.flag_info:
                            self.flag_info = False
                        else:
                            self.flag_info = True   



                    ##-----------------------------------------------------------
                    ##-----------------------------------------------------------
                    ########## GERE LES EVENEMENTS DE LA windowscan module
                    elif self.module.buton_undoRect.collidepoint(event.pos): # BUTON UNDO
                        if len(self.parcel.tour) > 0:
                            self.list_undo.append(self.parcel.tour.pop())
                    elif self.module.buton_redoRect.collidepoint(event.pos): # BUTON REDO
                        if len(self.list_undo) > 0:
                            self.parcel.tour.append(self.list_undo.pop())
                    elif self.module.buton_delRect.collidepoint(event.pos):
                        self.windowalerte = windowalerte.WindowAlerte(self.screen, "voulez vous detruire le tour ","de la parcelle")  # creer la fenetre d'alerte
                        if self.windowalerte.update():  # attente de reponse de la fenetre d'alerte
                            while len(self.parcel.tour) > 0:
                                self.list_undo.append(self.parcel.tour.pop())
                    elif self.module.buton_saveRect.collidepoint(event.pos):
                        self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.screen.blit(self.libelle_saving, self.libelle_savingRect)
                        pygame.display.update()
                        time.sleep(TIME_MSG)

                    ########## ON RETURN AU FICHIER windowscan POUR CHANGER DE MODULE ###########
                    elif self.module.buton_gRect.collidepoint(event.pos):
                        return -1 # on return au fichier windowscan.py pour changer de module
                    elif self.module.buton_dRect.collidepoint(event.pos):

                        return 1  # on return au fichier windowscan.py pour changer de module

                    ########## GERE LES EVENEMENTS DE LA window.main
                    ########## CHANGEMENT DE PARCELLE #################
                    elif self.window_main.bouton_parcelle_gRect.collidepoint(event.pos):  # change de parcelle
                        self.index_scan_mode = 0  # on repasse en mode VIEW
                        self.scan_mode()
                        self.list_undo = []
                        #self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.window_main.dec_index_parcelle()
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet
                    elif self.window_main.bouton_parcelle_dRect.collidepoint(event.pos):  # change de parcelle
                        self.index_scan_mode = 0  # on repasse en mode VIEW
                        self.scan_mode()
                        self.list_undo = []
                        #self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.window_main.inc_index_parcelle()
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet

                    retour = self.window_main.gest_event(event, self.parcel)
                    if retour == 0 : # si l'ACTION change return a windowscan et return a main.py 
                        return 0

