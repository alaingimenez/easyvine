# windowpassage

"""
ici on pourra juste tracer les endroits ou l'on passe dans la vigne pour savoir se qui a été fait
et on pourat sauvegarder ce qui a ete fait

on pourra faire des passage dans une vigne non scanne il suffirat de rentrer la largeur des rangs
et le logiciel calculera le nombre de rang a condition de faire un passage dans le premier et dernier rang

"""



import config
import parcelle

import pygame
pygame.init()


class WindowPassage:
    def __init__(self, window_m):

        self.window_main = window_m
        self.screen = self.window_main.screen
        self.parcel = parcelle.Parcelle
        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet

        self.font_g = pygame.font.Font('freesansbold.ttf', 80)


        self.libelle_general = self.font_g.render("PASSAGE ROUTINE NON IMPLANTE", True, config.WHITE, config.BLACK)
        self.libelle_generalRect = self.libelle_general.get_rect()
        self.libelle_generalRect.x = 10
        self.libelle_generalRect.y = 200

        self.flag_info = False


        self.update()

    def update(self):
        self.screen.blit(self.libelle_general, self.libelle_generalRect)



    def gestion(self):
        while True:
            titre = "** EasyVine PASSAGE**  "  # lat: " + format(self.latitude, '.7f') + "   long: " + format(self.longitude, '.7f') + "  track: " + format(self.track,'.2f') + "  altitude: " + format(self.altitude, '.4f')
            pygame.display.set_caption(titre) 
            pygame.Surface.fill(self.screen, config.BLACK)


            ########################################### AFFICHE LES MENUS ##############################
            self.window_main.update()  # # affiche a l'ecran les texte
            self.update()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window_main.index_action = -99 # permet de fermer le programe
                    
                    return 0  # 
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
                        #self.premier_passage_boucle = True
                        #self.count_evenement()

                    elif self.window_main.bouton_parcelle_dRect.collidepoint(event.pos):  # change de parcelle
                        #self.window_main.fichier.save_file(self.window_main.name_parcelle, self.parcel)
                        self.evenement_pyg = []
                        self.window_main.inc_index_parcelle()
                        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle)  # charge un objet
                        #self.premier_passage_boucle = True
                        #self.count_evenement()
                        


                    retour = self.window_main.gest_event(event, self.parcel)
                    if retour == 0 : # si l'ACTION change  et return a main.py 
                        return 0