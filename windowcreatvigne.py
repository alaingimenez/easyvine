#windowcreatvigne


import config
import main


import pygame
pygame.init()







class WindowCreatVigne:
    def __init__(self, window_m, module, parcel):

        self.window_main = window_m
        self.screen = self.window_main.screen
        self.module = module
        self.parcel = parcel
        
        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet
        

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_g = pygame.font.Font('freesansbold.ttf', 80)

        self.libelle_general = self.font_g.render("CREAT VIGNE NON IMPLANTE", True, config.WHITE, config.BLACK)
        self.libelle_generalRect = self.libelle_general.get_rect()
        self.libelle_generalRect.x = 10
        self.libelle_generalRect.y = 200

        self.latitude = 0
        self.longitude = 0
        self.position_gps = (self.latitude, self.longitude)
        self.track = 0
        self.altitude_gps = 0

        self.update()


    def update(self):
        self.screen.blit(self.libelle_general,self.libelle_generalRect)



    def gestion(self):
        gs = main.GpsPoller()
        gs.start() # start it up



        while True:

            self.latitude = gs.gpsd.fix.latitude
            self.longitude = gs.gpsd.fix.longitude
            self.position_gps = (self.latitude, self.longitude)
            self.track = gs.gpsd.fix.track
            self.altitude_gps = gs.gpsd.fix.altitude


            titre = "**EasyVine CREAT VIGNE **   lat: " + format(self.latitude, '.7f') + "   long: " + format(self.longitude, '.7f') + "  track: " + format(self.track,'.2f')  # + "  altitude: " + format(self.altitude, '.4f')
            pygame.display.set_caption(titre)

            pygame.Surface.fill(self.screen, config.BLACK)



            ########################################### AFFICHE LES MENUS ##############################
            self.window_main.update()  # # affiche a l'ecran les texte
            self.module.update()
            self.update()
            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   
                    self.window_main.index_action = -99 # permet de fermer le programe
                    gs.running = False
                    gs.join() # wait for the thread to finish what it's doing
                    del(gs)
                    return 0  # return windowrecherch
                
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    ########## ON RETURN AU FICHIER windowcreat POUR CHANGER DE MODULE ###########
                    if self.module.buton_gRect.collidepoint(event.pos):
                        return -1 # on return au fichier windowcreat.py pour changer de module
                    elif self.module.buton_dRect.collidepoint(event.pos):
                        return 1  # on return au fichier windowcreat.py pour changer de module

                    ########## GERE LES EVENEMENTS DE LA window.main
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
                    if retour == 0 : # si l'ACTION change return a windowcreat et return a main.py 
                        return 0