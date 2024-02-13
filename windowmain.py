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

"""
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(config.PIN_NO_RTK,GPIO.IN, pull_up_down = GPIO.PUD_UP)

import gpiozero
# no_rtk = gpiozero.Button(PIN_NO_RTK, pull_up= False)  dans se cas pull_up est DOWN
no_rtk = gpiozero.Button(config.PIN_NO_RTK)
"""

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

        self.actions = [" FICHIER  ", " CREAT ", "MODIFY", "DELETE", " SCAN ", " _VIEW_ ", "RECHERCHER", "  TRAVAIL  "," PASSAGE"]#[" FICHIER  ", " CREAT ", " SCAN ", " _VIEW_ ", "RECHERCHER", "  OUTILS  "]
        """
        action FICHIER permet de CREER ET EFFACER des fichier de vigne  ou de robot
        action OBJET permet de creer des VIGNE des PORTEUR des OUTIL
        action SCAN permeet de scanner des PARCELLE des RANG des EVENEMENT
        action RECHERCHE permet de rechercher des evenements et de faire un parcour qui méne au evenement
        action OUTILS permet de creer des parcour pour des outil TONDEUSE DK ARROSEUSE EPEMPREUSE etc et simuler les parcours
        """
        self.index_action = 5


        


        self.zoom = 1
        self.zoom1 = 0.50
        self.zoom2 = 3
        self.zoom3 = 5
        self.zoom4 = 7

        self.centre_x = 500
        self.centre_y = 500

        self.libelle_vigne = self.font_p.render("Vigne encours", True, config.WHITE, config.BLACK)
        self.libelle_vigneRect = self.libelle_vigne.get_rect()
        self.libelle_vigneRect.x = 100
        self.libelle_vigneRect.y = 935

        dec_act = 350
        self.libelle_action = self.font_p.render("Action", True, config.WHITE, config.BLACK)
        self.libelle_actionRect = self.libelle_action.get_rect()
        self.libelle_actionRect.x = 750 + dec_act
        self.libelle_actionRect.y = 935 

        self.bouton_action_g = self.font.render(str("<< :"), True, config.YELLOW, config.GRAY)  # transformer le texte en graphique
        self.bouton_action_gRect = self.bouton_action_g.get_rect()
        self.bouton_action_gRect.x = 670 + dec_act # position le texte en width
        self.bouton_action_gRect.y = 960   # position le texe en heigh en se servant de sa hauteur

        self.bouton_action_d = self.font.render(str(": >>"), True, config.YELLOW, config.GRAY)  # transformer le texte en graphique
        self.bouton_action_dRect = self.bouton_action_d.get_rect()
        self.bouton_action_dRect.x = 940 + dec_act # position le texte en width
        self.bouton_action_dRect.y = 960  # position le texe en heigh en se servant de sa hauteur

        self.name_action = self.actions[self.index_action]  # chargement de la liste /PARCELLE/ /RANG/
        self.text_action = self.font.render(str(self.name_action), True, config.GREEN,
                                            config.BLUE)  # transformer le texte en graphique
        self.text_actionRect = self.text_action.get_rect()  # recuperer le rectangle du texte
        self.text_actionRect.x = 730 + dec_act # position le texte 10 + largeur  bouton gauche  + 5 en width
        self.text_actionRect.y = 960   # position le texe en heigh en se servant de sa hauteur


        self.bouton_parcelle_g = self.font.render("<< :", True, config.YELLOW, config.GRAY)
        self.bouton_parcelle_gRect = self.bouton_parcelle_g.get_rect()
        self.bouton_parcelle_gRect.x = 10
        self.bouton_parcelle_gRect.y = 960

        self.bouton_parcelle_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.bouton_parcelle_dRect = self.bouton_parcelle_d.get_rect()
        self.bouton_parcelle_dRect.x = 250
        self.bouton_parcelle_dRect.y = 960

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
        self.buton_zoom_gRect.x = 320
        self.buton_zoom_gRect.y = 960

        self.buton_zoom_d = self.font.render(": >>", True, config.YELLOW, config.GRAY)
        self.buton_zoom_dRect = self.buton_zoom_d.get_rect()
        self.buton_zoom_dRect.x = 455
        self.buton_zoom_dRect.y = 960

        self.text_zoom = self.font.render(format(self.zoom,'.2f'), True, config.GREEN, config.BLUE)
        self.text_zoom_Rect = self.text_zoom.get_rect()
        self.text_zoom_Rect.x = 380
        self.text_zoom_Rect.y = 960

        
        self.libelle_zoom = self.font_p.render("|ZOOM|", True, config.YELLOW, config.GRAY)
        self.libelle_zoomRect = self.libelle_zoom.get_rect()
        self.libelle_zoomRect.x = 375
        self.libelle_zoomRect.y = 925

        dec_zoom = 510
        self.btn_zoom1= self.font_p.render("|ZOOM 1|", True, config.YELLOW, config.GRAY)
        self.btn_zoom1Rect = self.btn_zoom1.get_rect()
        self.btn_zoom1Rect.x = 1020 - dec_zoom
        self.btn_zoom1Rect.y = 925
     
        self.txt_zoom1= self.font_p.render(format(self.zoom1,'.2f'), True, config.YELLOW, config.GRAY)
        self.txt_zoom1Rect = self.txt_zoom1.get_rect()
        self.txt_zoom1Rect.x = 1040 - dec_zoom
        self.txt_zoom1Rect.y = 960 

        self.btn_zoom2= self.font_p.render("|ZOOM 2|", True, config.YELLOW, config.GRAY)
        self.btn_zoom2Rect = self.btn_zoom2.get_rect()
        self.btn_zoom2Rect.x = 1020 + 120 - dec_zoom
        self.btn_zoom2Rect.y = 925

        self.txt_zoom2= self.font_p.render(format(self.zoom2,'.2f'), True, config.YELLOW, config.GRAY)
        self.txt_zoom2Rect = self.txt_zoom2.get_rect()
        self.txt_zoom2Rect.x = 1040 + 120 - dec_zoom
        self.txt_zoom2Rect.y = 960

        self.btn_zoom3= self.font_p.render("|ZOOM 3|", True, config.YELLOW, config.GRAY)
        self.btn_zoom3Rect = self.btn_zoom3.get_rect()
        self.btn_zoom3Rect.x = 1020 + 240- dec_zoom
        self.btn_zoom3Rect.y = 925

        self.txt_zoom3= self.font_p.render(format(self.zoom3,'.2f'), True, config.YELLOW, config.GRAY)
        self.txt_zoom3Rect = self.txt_zoom3.get_rect()
        self.txt_zoom3Rect.x = 1040 +240 - dec_zoom
        self.txt_zoom3Rect.y = 960

        self.btn_zoom4= self.font_p.render("|ZOOM 4|", True, config.YELLOW, config.GRAY)
        self.btn_zoom4Rect = self.btn_zoom4.get_rect()
        self.btn_zoom4Rect.x = 1020 + 360 - dec_zoom
        self.btn_zoom4Rect.y = 925

        self.txt_zoom4= self.font_p.render(format(self.zoom4,'.2f'), True, config.YELLOW, config.GRAY)
        self.txt_zoom4Rect = self.txt_zoom4.get_rect()
        self.txt_zoom4Rect.x = 1040 + 360 - dec_zoom
        self.txt_zoom4Rect.y = 960

        self.text_rtk = self.font.render("NO RTK", True, config.BLACK, config.RED)
        self.text_rtk_Rect = self.text_rtk.get_rect()
        self.text_rtk_Rect.x = 1360
        self.text_rtk_Rect.y = 960

        self.buton_quit = self.font.render("QUIT", True, config.YELLOW, config.GRAY)
        self.buton_quitRect = self.buton_quit.get_rect()
        self.buton_quitRect.x = 1400
        self.buton_quitRect.y = 915

        self.buton_info = self.font.render("| INFO |", True, config.YELLOW, config.GRAY)
        self.buton_infoRect = self.buton_info.get_rect()
        self.buton_infoRect.x = 160
        self.buton_infoRect.y = 884

        # variable pour faire clignoter PI_RASPI_OK
        self.val_raspi_ok = 25
        self.compteur_raspi_ok = self.val_raspi_ok

        self.temperature = 0
        self.text_temp = self.font_p.render(format(self.temperature,'.2f'), True, config.BLACK, config.GRAY)
        self.text_tempRect = self.text_temp .get_rect()
        self.text_tempRect.x = 1430
        self.text_tempRect.y = 880

        self.update()

    def update(self):
        self.screen.blit(self.buton_info, self.buton_infoRect)
        self.screen.blit(self.libelle_zoom, self.libelle_zoomRect)
        self.text_zoom = self.font.render(format(self.zoom, '.2f'), True, config.GREEN, config.BLUE)
        self.screen.blit(self.text_zoom, self.text_zoom_Rect)
        self.screen.blit(self.buton_zoom_g, self.buton_zoom_gRect)
        self.screen.blit(self.buton_zoom_d, self.buton_zoom_dRect)

        self.screen.blit(self.btn_zoom1, self.btn_zoom1Rect)
        self.txt_zoom1 = self.font.render(format(self.zoom1, '.2f'), True, config.YELLOW, config.GRAY)
        self.screen.blit(self.txt_zoom1, self.txt_zoom1Rect)

        self.screen.blit(self.btn_zoom2, self.btn_zoom2Rect)
        self.txt_zoom2 = self.font.render(format(self.zoom2, '.2f'), True, config.YELLOW, config.GRAY)
        self.screen.blit(self.txt_zoom2, self.txt_zoom2Rect)

        self.screen.blit(self.btn_zoom3, self.btn_zoom3Rect)
        self.txt_zoom3 = self.font.render(format(self.zoom3, '.2f'), True, config.YELLOW, config.GRAY)
        self.screen.blit(self.txt_zoom3, self.txt_zoom3Rect)

        self.screen.blit(self.btn_zoom4, self.btn_zoom4Rect)
        self.txt_zoom4 = self.font.render(format(self.zoom4, '.2f'), True, config.YELLOW, config.GRAY)
        self.screen.blit(self.txt_zoom4, self.txt_zoom4Rect)

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

        #if(GPIO.input(config.PIN_NO_RTK)):
        if not config.NO_RTK.is_pressed:    
            self.text_rtk = self.font.render("NO RTK", True, config.BLACK, config.RED)
        else:
            self.text_rtk = self.font.render("RTK OK", True, config.BLACK, config.GREEN)
        
        self.screen.blit(self.text_rtk, self.text_rtk_Rect)
        self.screen.blit(self.buton_quit, self.buton_quitRect)

        # print("c'est ici qu'il faut faire clignoter la del")
        self.compteur_raspi_ok = self.compteur_raspi_ok - 1
        if self.compteur_raspi_ok == 0:
            self.compteur_raspi_ok = self.val_raspi_ok
            config.RASPI_OK.toggle()
            
        # AFFICHER LA TEMPERATURE Du RASPBERRY
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as ftemp:
            self.temperature = int(ftemp.read()) / 1000
            temp =int(self.temperature)
            self.text_temp = self.font_p.render(str(temp)+"°", True, config.BLACK, config.GRAY)
            #self.text_temp = self.font_p.render(format(self.temperature,'.0f'), True, config.WHITE, config.GRAY)
            self.screen.blit(self.text_temp, self.text_tempRect)

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
        if self.buton_quitRect.collidepoint(event.pos):
            self.index_action = -99 # permet de fermer le programe
            print("JE QUITE LE PROGRAME")
            return 0
        ############# GESTION DU CENTRAGE ##################
        elif self.buton_centre_hRect.collidepoint(event.pos):
            self.centre_y -= 200

        elif self.buton_centre_bRect.collidepoint(event.pos):
            self.centre_y += 200

        elif self.buton_centre_gRect.collidepoint(event.pos):
            self.centre_x -= 200
        elif self.buton_centre_dRect.collidepoint(event.pos):
            self.centre_x += 200
        elif self.buton_centreRect.collidepoint(event.pos):
            self.centre_x = 500
            self.centre_y = 500 # centrer la parcelle de maniere a la voir en totalité

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
        elif self.libelle_zoomRect.collidepoint(event.pos):
            self.zoom = 1
        elif self.btn_zoom1Rect.collidepoint(event.pos):
            self.zoom = self.zoom1
        elif self.btn_zoom2Rect.collidepoint(event.pos):
            self.zoom = self.zoom2
        elif self.btn_zoom3Rect.collidepoint(event.pos):
            self.zoom = self.zoom3
        elif self.btn_zoom4Rect.collidepoint(event.pos):
            self.zoom = self.zoom4

        elif self.txt_zoom1Rect.collidepoint(event.pos):
            self.zoom1 = self.zoom
        elif self.txt_zoom2Rect.collidepoint(event.pos):
            self.zoom2 = self.zoom
        elif self.txt_zoom3Rect.collidepoint(event.pos):
            self.zoom3 = self.zoom
        elif self.txt_zoom4Rect.collidepoint(event.pos):
            self.zoom4 = self.zoom
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