"""
menu pour selectionner si on va dans :
fichier Creat
ou
Fichier Delete
"""


import config
import fichier

import pygame
pygame.init()




DELAY = 0.2



class WindowMain:
    def __init__(self, screen):
        self.screen = screen

        self.fichier = fichier.Fichier()
        self.list_name_parcelle = self.fichier.get_list() # recupere la liste des fichier qu'il y a sur le disk
        self.index_list_name_parcelle = 0
        self.name_parcelle = self.list_name_parcelle[self.index_list_name_parcelle]

        self.titre_window = "fenetre principale"
        self.font_p = pygame.font.Font('freesansbold.ttf', 25)
        self.font = pygame.font.Font('freesansbold.ttf', 30)

        self.actions = [" FICHIER  ", " CREAT ", " SCAN ", " _VIEW_ ", "RECHERCHER", "  OUTILS  "]
        """
        action FICHIER permet de CREER ET EFFACER des fichier
        action CREAT permet de creer des PARCELLE et des RANG
        action SCAN permeet de scanner des PARCELLE des RANG des EVENEMENT
        action OUTILS permet de creer des parcour pour des outil TONDEUSE DK ARROSEUSE EPEMPREUSE etc et simuler les parcours
        """
        self.index_action = 0


        self.zoom = 1
        self.centre_x = 500
        self.centre_y = 500

        self.libelle_vigne = self.font_p.render("Vigne encours", True, config.WHITE, config.BLACK)
        self.libelle_vigneRect = self.libelle_vigne.get_rect()
        self.libelle_vigneRect.x = 100
        self.libelle_vigneRect.y = 935

        self.libelle_action = self.font_p.render("Action", True, config.WHITE, config.BLACK)
        self.libelle_actionRect = self.libelle_action.get_rect()
        self.libelle_actionRect.x = 750
        self.libelle_actionRect.y = 935


        self.bouton_action_g = self.font.render(str("<< :"), True, config.YELLOW, config.GRAY)  # transformer le texte en graphique
        self.bouton_action_gRect = self.bouton_action_g.get_rect()
        self.bouton_action_gRect.x = 670 # position le texte en width
        self.bouton_action_gRect.y = 960  # position le texe en heigh en se servant de sa hauteur

        self.bouton_action_d = self.font.render(str(": >>"), True, config.YELLOW, config.GRAY)  # transformer le texte en graphique
        self.bouton_action_dRect = self.bouton_action_d.get_rect()
        self.bouton_action_dRect.x = 940  # position le texte en width
        self.bouton_action_dRect.y = 960  # position le texe en heigh en se servant de sa hauteur

        self.bouton_parcelle_g = self.font.render("<< :", True, config.YELLOW, config.GRAY)
        self.bouton_parcelle_gRect = self.bouton_parcelle_g.get_rect()
        self.bouton_parcelle_gRect.x = 10
        self.bouton_parcelle_gRect.y = 960

        self.bouton_parcelle_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.bouton_parcelle_dRect = self.bouton_parcelle_d.get_rect()
        self.bouton_parcelle_dRect.x = 250
        self.bouton_parcelle_dRect.y = 960

        self.name_action = self.actions[self.index_action]  # chargement de la liste /PARCELLE/ /RANG/
        self.text_action = self.font.render(str(self.name_action), True, config.GREEN,
                                            config.BLUE)  # transformer le texte en graphique
        self.text_actionRect = self.text_action.get_rect()  # recuperer le rectangle du texte
        self.text_actionRect.x = 730  # position le texte 10 + largeur  bouton gauche  + 5 en width
        self.text_actionRect.y = 960  # position le texe en heigh en se servant de sa hauteur

        self.name_parcelle = self.list_name_parcelle[self.index_list_name_parcelle]
        self.text_name_parcelle = self.font.render(self.name_parcelle, True, config.GREEN, config.BLUE)
        self.text_name_parcelleRect = self.text_name_parcelle.get_rect()
        self.text_name_parcelleRect.x = 80
        self.text_name_parcelleRect.y = 960

        self.buton_centre_h = self.font.render("^^", True, config.YELLOW, config.GRAY)
        self.buton_centre_hRect = self.buton_centre_h.get_rect()
        self.buton_centre_hRect.x = 50
        self.buton_centre_hRect.y = 850

        self.buton_centre = self.font.render("@", True, config.YELLOW, config.GRAY)
        self.buton_centreRect = self.buton_centre.get_rect()
        self.buton_centreRect.x = 52
        self.buton_centreRect.y = 884

        self.buton_centre_b = self.font.render("vv", True, config.YELLOW, config.GRAY)
        self.buton_centre_bRect = self.buton_centre_b.get_rect()
        self.buton_centre_bRect.x = 50
        self.buton_centre_bRect.y = 920

        self.buton_centre_g = self.font.render("<<", True, config.YELLOW, config.GRAY)
        self.buton_centre_gRect = self.buton_centre_g.get_rect()
        self.buton_centre_gRect.x = 10
        self.buton_centre_gRect.y = 884

        self.buton_centre_d = self.font.render(">>", True, config.YELLOW, config.GRAY)
        self.buton_centre_dRect = self.buton_centre_d.get_rect()
        self.buton_centre_dRect.x = 86
        self.buton_centre_dRect.y = 884

        self.buton_zoom_g = self.font.render("<< :", True, config.YELLOW, config.GRAY)
        self.buton_zoom_gRect = self.buton_zoom_g.get_rect()
        self.buton_zoom_gRect.x = 340
        self.buton_zoom_gRect.y = 960

        self.buton_zoom_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.buton_zoom_dRect = self.buton_zoom_d.get_rect()
        self.buton_zoom_dRect.x = 465
        self.buton_zoom_dRect.y = 960

        self.text_zoom = self.font.render(format(self.zoom,'.2f'), True, config.GREEN, config.BLUE)
        self.text_zoom_Rect = self.text_zoom.get_rect()
        self.text_zoom_Rect.x = 400
        self.text_zoom_Rect.y = 960

        self.libelle_zoom = self.font_p.render("ZOOM", True, config.WHITE, config.BLACK)
        self.libelle_zoomRect = self.libelle_zoom.get_rect()
        self.libelle_zoomRect.x = 395
        self.libelle_zoomRect.y = 935

        self.buton_info = self.font.render("| INFO |", True, config.YELLOW, config.GRAY)
        self.buton_infoRect = self.buton_info.get_rect()
        self.buton_infoRect.x = 160
        self.buton_infoRect.y = 884

        self.update()

    def update(self):
        self.screen.blit(self.buton_info, self.buton_infoRect)
        self.screen.blit(self.libelle_zoom, self.libelle_zoomRect)
        self.text_zoom = self.font.render(format(self.zoom, '.2f'), True, config.GREEN, config.BLUE)
        self.screen.blit(self.text_zoom, self.text_zoom_Rect)
        self.screen.blit(self.buton_zoom_g, self.buton_zoom_gRect)
        self.screen.blit(self.buton_zoom_d, self.buton_zoom_dRect)
        self.screen.blit(self.buton_centre_h, self.buton_centre_hRect)
        self.screen.blit(self.buton_centre_d, self.buton_centre_dRect)
        self.screen.blit(self.buton_centre_g, self.buton_centre_gRect)
        self.screen.blit(self.buton_centre_b, self.buton_centre_bRect)
        self.screen.blit(self.buton_centre, self.buton_centreRect)
        self.screen.blit(self.libelle_vigne, self.libelle_vigneRect)
        self.screen.blit(self.libelle_action, self.libelle_actionRect)
        self.screen.blit(self.bouton_action_g, self.bouton_action_gRect)
        self.screen.blit(self.bouton_action_d,self.bouton_action_dRect)
        self.screen.blit(self.text_action,self.text_actionRect)
        self.screen.blit(self.bouton_parcelle_g, self.bouton_parcelle_gRect )
        self.screen.blit(self.bouton_parcelle_d, self.bouton_parcelle_dRect)

        self.name_action = self.actions[self.index_action]  # chargement de la liste /PARCELLE/ /RANG/
        self.text_action = self.font.render(str(self.name_action), True, config.GREEN,
                                            config.BLUE)  # transformer le texte en graphique
        self.screen.blit(self.text_action, self.text_actionRect)

        self.name_parcelle = self.list_name_parcelle[self.index_list_name_parcelle]
        self.text_name_parcelle = self.font.render(self.name_parcelle, True, config.GREEN, config.BLUE)
        self.screen.blit(self.text_name_parcelle, self.text_name_parcelleRect)



    def inc_action_actuelle(self):
        self.index_action += 1
        if self.index_action == len(self.actions):
            self.index_action = 0
        self.update()
        return self.index_action

    def dec_action_actuelle(self):
        self.index_action -= 1
        if self.index_action == -1:
            self.index_action = len(self.actions) - 1
        self.update()
        return self.index_action

    def inc_index_parcelle(self):
        self.index_list_name_parcelle += 1
        if self.index_list_name_parcelle == len(self.list_name_parcelle):
            self.index_list_name_parcelle = 0
        self.update()
        return self.index_list_name_parcelle

    def dec_index_parcelle(self):
        self.index_list_name_parcelle -= 1
        if self.index_list_name_parcelle == -1:
            self.index_list_name_parcelle = len(self.list_name_parcelle) -1
        self.update()
        return self.index_list_name_parcelle

    ############### GESTION DES EVENEMENTS ##############################
    def gest_event(self,event,parcel):
        ############# GESTION DU CENTRAGE ##################
        if self.buton_centre_hRect.collidepoint(event.pos):
            self.centre_y -= 10

        elif self.buton_centre_bRect.collidepoint(event.pos):
            self.centre_y += 10

        elif self.buton_centre_gRect.collidepoint(event.pos):
            self.centre_x -= 10
        elif self.buton_centre_dRect.collidepoint(event.pos):
            self.centre_x += 10
        elif self.buton_centreRect.collidepoint(event.pos):
            pass  # centrer la parcelle de maniere a la voir en totalité

        ############### GESTION DU ZOOM ###############
        elif self.buton_zoom_dRect.collidepoint(event.pos):
            if self.zoom <= 0.30:
                self.zoom += 0.01
            elif self.zoom <= 2:
                self.zoom += 0.20
            else:
                self.zoom += 1
        elif self.buton_zoom_gRect.collidepoint(event.pos):
            if self.zoom <= 0.30:
                self.zoom -= 0.01
            elif self.zoom <= 2:
                self.zoom -= 0.20
            else:
                self.zoom -= 1
            if self.zoom <= 0:
                self.zoom = 0.01

        ################# CHANGE L'ACTION ############################################
        elif self.bouton_action_gRect.collidepoint(event.pos):  # permet de sortir de la windowscan
            self.dec_action_actuelle()
            self.update()  # # affiche a l'ecran les texte
            self.fichier.save_file(self.name_parcelle, parcel)
            return 0
        elif self.bouton_action_dRect.collidepoint(event.pos):  # permet de sortir de la windowscan en chang l'action
            self.inc_action_actuelle()
            self.update()  # # affiche a l'ecran les texte
            self.fichier.save_file(self.name_parcelle, parcel)
            return 0