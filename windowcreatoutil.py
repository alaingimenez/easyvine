#windowcreatoutil



import config
import main


import pygame
pygame.init()







class WindowCreatOutil:
    def __init__(self, window_m, module, parcel):

        self.window_main = window_m
        self.screen = self.window_main.screen
        self.module = module
        self.parcel = parcel
        

        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_g = pygame.font.Font('freesansbold.ttf', 80)

        self.libelle_nom = self.font.render("NOM DE L'OUTIL :", True, config.WHITE, config.BLACK)
        self.libelle_nomRect = self.libelle_nom.get_rect()
        self.libelle_nomRect.x = 10
        self.libelle_nomRect.y = 80 

        self.nom =""
        self.btn_nom = self.font.render("|" + self.nom + "|", True, config.YELLOW, config.GRAY)
        self.btn_nomRect = self.btn_nom.get_rect()
        self.btn_nomRect.x = 280
        self.btn_nomRect.y = 80

        self.libelle_largeur_travail = self.font.render("LARGEUR DE TRAVAIL ", True, config.WHITE, config.BLACK)
        self.libelle_largeur_travailRect = self.libelle_largeur_travail.get_rect()
        self.libelle_largeur_travailRect.x = 10
        self.libelle_largeur_travailRect.y = 420

        self.largeur_travail = ""
        self.btn_largeur_travail= self.font.render("|" + self.largeur_travail + "|", True, config.YELLOW, config.GRAY)
        self.btn_largeur_travailRect = self.btn_largeur_travail.get_rect()
        self.btn_largeur_travailRect.x = 280
        self.btn_largeur_travailRect.y = 420

        self.libelle_longeur_outil = self.font.render("LONGUEUR OUTIL ", True, config.WHITE, config.BLACK)
        self.libelle_longeur_outilRect = self.libelle_longeur_outil.get_rect()
        self.libelle_longeur_outilRect.x = 10
        self.libelle_longeur_outilRect.y = 460

        self.longueur_outil = ""
        self.btn_longueur_outil = self.font.render("|" + self.longueur_outil + "|", True, config.YELLOW, config.GRAY)
        self.btn_longueur_outilRect = self.btn_longueur_outil.get_rect()
        self.btn_longueur_outilRect.x = 280
        self.btn_longueur_outilRect.y = 460

        self.libelle_distance_gps_debut_outil = self.font.render("DISTANCE GPS DEBUT OUTIL ", True, config.WHITE, config.BLACK)
        self.libelle_distance_gps_debut_outilRect = self.libelle_distance_gps_debut_outil.get_rect()
        self.libelle_distance_gps_debut_outilRect.x = 10
        self.libelle_distance_gps_debut_outilRect.y = 500

        self.distance_gps_debut_outil =""
        self.btn_distance_gps_debut_outil = self.font.render("|" + self.distance_gps_debut_outil+ "|", True, config.YELLOW, config.GRAY)
        self.btn_distance_gps_debut_outilRect = self.btn_distance_gps_debut_outil.get_rect()
        self.btn_distance_gps_debut_outilRect.x = 280
        self.btn_distance_gps_debut_outilRect.y = 500

        self.libelle_distance_gps_exterieur_outil = self.font.render("DISTANCE GPS EXTERIEUR OUTIL ", True, config.WHITE, config.BLACK)
        self.libelle_distance_gps_exterieur_outilRect = self.libelle_distance_gps_exterieur_outil.get_rect()
        self.libelle_distance_gps_exterieur_outilRect.x = 10
        self.libelle_distance_gps_exterieur_outilRect.y = 540

        self.distance_gps_exterieur_outil = ""
        self.btn_distance_gps_exterieur_outil = self.font.render("|" + self.distance_gps_exterieur_outil + "|", True, config.YELLOW, config.GRAY)
        self.btn_distance_gps_exterieur_outilRect = self.btn_distance_gps_exterieur_outil.get_rect()
        self.btn_distance_gps_exterieur_outilRect.x = 280
        self.btn_distance_gps_exterieur_outilRect.y = 540

        self.libelle_penetration_in_intercep= self.font.render("PENETRATION DANS L'INTERCEP ", True, config.WHITE, config.BLACK)
        self.libelle_penetration_in_intercepRect = self.libelle_penetration_in_intercep.get_rect()
        self.libelle_penetration_in_intercepRect.x = 10
        self.libelle_penetration_in_intercepRect.y = 580

        self.penetration_in_intercep = ""
        self.btn_penetration_in_intercep = self.font.render("|" + self.penetration_in_intercep + "|", True, config.YELLOW, config.GRAY)
        self.btn_penetration_in_intercepRect = self.btn_penetration_in_intercep.get_rect()
        self.btn_penetration_in_intercepRect.x = 280
        self.btn_penetration_in_intercepRect.y = 580

        """
        self.libelle_hauteur_antene_gps = self.font.render("Hauteur GPS: ", True, config.WHITE, config.BLACK)
        self.libelle_hauteur_antene_gpsRect = self.libelle_hauteur_antene_gps.get_rect()
        self.libelle_hauteur_antene_gpsRect.x = 10
        self.libelle_hauteur_antene_gpsRect.y = 620
        
        self.hauteur_gps = ""
        self.btn_hauteur_gps = self.font.render("|" + self.hauteur_gps + "|", True, config.YELLOW, config.GRAY)
        self.btn_hauteur_gpsRect = self.btn_hauteur_gps.get_rect()
        self.btn_hauteur_gpsRect.x = 280
        self.btn_hauteur_gpsRect.y = 620
    
        self.libelle_vitesse_max = self.font.render("Vitesse Max: ", True, config.WHITE, config.BLACK)
        self.libelle_vitesse_maxRect = self.libelle_vitesse_max.get_rect()
        self.libelle_vitesse_maxRect.x = 10
        self.libelle_vitesse_maxRect.y = 660

        self.vitesse_max = ""
        self.btn_vitesse_max = self.font.render("|" + self.vitesse_max + "|", True, config.YELLOW, config.GRAY)
        self.btn_vitesse_maxRect = self.btn_vitesse_max.get_rect()
        self.btn_vitesse_maxRect.x = 280
        self.btn_vitesse_maxRect.y = 660
        """


        self.list_type = config.LIST_TYPE_OUTILS
        self.index_type = 0
        

        self.libelle_type= self.font.render("TYPE : ", True, config.WHITE, config.BLACK)
        self.libelle_typeRect = self.libelle_type.get_rect()
        self.libelle_typeRect.x = 10
        self.libelle_typeRect.y = 120

        a = 100
        self.type = self.font.render(self.list_type[self.index_type], True, config.GREEN, config.BLUE)
        self.typeRect = self.type.get_rect()
        self.typeRect.x = 260 + a
        self.typeRect.y = 120

        self.btn_dec_type = self.font.render("<<:", True, config.YELLOW, config.GRAY)
        self.btn_dec_typeRect = self.btn_dec_type.get_rect()
        self.btn_dec_typeRect.x = 210 + a
        self.btn_dec_typeRect.y = 120

        self.btn_inc_type = self.font.render(":>>", True, config.YELLOW, config.GRAY)
        self.btn_inc_typeRect = self.btn_inc_type.get_rect()
        self.btn_inc_typeRect.x = 670 + a + 50
        self.btn_inc_typeRect.y = 120

        self.list_partie_travaille = config.PARTIE_TRAVAILLE_PAR_LOUTIL
        self.index_partie_travaille  = 0
        

        self.libelle_partie_travaille  = self.font.render("PARTIE TRAVAILLE ", True, config.WHITE, config.BLACK)
        self.libelle_partie_travailleRect = self.libelle_partie_travaille .get_rect()
        self.libelle_partie_travailleRect.x = 10
        self.libelle_partie_travailleRect.y = 160

        self.partie_travaille  = self.font.render(self.list_partie_travaille [self.index_partie_travaille ], True, config.GREEN, config.BLUE)
        self.partie_travailleRect = self.partie_travaille .get_rect()
        self.partie_travailleRect.x = 260 + a
        self.partie_travailleRect.y = 160

        self.btn_dec_partie_travaille  = self.font.render("<<:", True, config.YELLOW, config.GRAY)
        self.btn_dec_partie_travailleRect = self.btn_dec_partie_travaille .get_rect()
        self.btn_dec_partie_travailleRect.x = 210 + a
        self.btn_dec_partie_travailleRect.y = 160

        self.btn_inc_partie_travaille  = self.font.render(":>>", True, config.YELLOW, config.GRAY)
        self.btn_inc_partie_travailleRect = self.btn_inc_partie_travaille .get_rect()
        self.btn_inc_partie_travailleRect.x = 670 + a + 50
        self.btn_inc_partie_travailleRect.y = 160

        self.list_relevage = config.LIST_NON_OUI
        self.index_relevage = 0
        

        self.libelle_relevage = self.font.render("OUTIL A RELEVAGE ", True, config.WHITE, config.BLACK)
        self.libelle_relevageRect = self.libelle_relevage.get_rect()
        self.libelle_relevageRect.x = 10
        self.libelle_relevageRect.y = 200

        self.btn_relevage = self.font.render(self.list_relevage[self.index_relevage], True, config.YELLOW, config.GRAY)
        self.btn_relevageRect = self.btn_relevage.get_rect()
        self.btn_relevageRect.x = 260 + 140
        self.btn_relevageRect.y = 200

        """
        self.btn_dec_choix_outil= self.font.render("<<:", True, config.YELLOW, config.GRAY)
        self.btn_dec_choix_outilRect = self.btn_dec_choix_outil.get_rect()
        self.btn_dec_choix_outilRect.x = 210 + 140
        self.btn_dec_choix_outilRect.y = 200

        self.btn_inc_choix_outil = self.font.render(":>>", True, config.YELLOW, config.GRAY)
        self.btn_inc_choix_outilRect = self.btn_inc_choix_outil.get_rect()
        self.btn_inc_choix_outilRect.x = 600 + 140
        self.btn_inc_choix_outilRect.y = 200
        
        self.btn_add_outil = self.font.render("v ADDS v",True, config.YELLOW, config.GRAY)
        self.btn_add_outilRect = self.btn_add_outil.get_rect()
        self.btn_add_outilRect.x = 280 + 100
        self.btn_add_outilRect.y = 590 

        self.btn_remove_outil = self.font.render("^ REMOVE ^",True, config.YELLOW, config.GRAY)
        self.btn_remove_outilRect = self.btn_remove_outil.get_rect()
        self.btn_remove_outilRect.x = 480 + 100
        self.btn_remove_outilRect.y = 590
        """
        self.list_action_au_cep = config.LIST_NON_OUI
        self.index_action_au_cep = 0
        
        self.libelle_action_au_cep = self.font.render("ACTION AU CEP : ", True, config.WHITE, config.BLACK)
        self.libelle_action_au_cepRect = self.libelle_action_au_cep.get_rect()
        self.libelle_action_au_cepRect.x = 10
        self.libelle_action_au_cepRect.y = 240

        self.btn_action_au_cep = self.font.render(self.list_action_au_cep[self.index_action_au_cep], True, config.GREEN, config.BLUE)
        self.btn_action_au_cepRect = self.btn_action_au_cep.get_rect()
        self.btn_action_au_cepRect.x = 260 + 140
        self.btn_action_au_cepRect.y = 240

        self.list_outil_a_tateur = config.LIST_NON_OUI
        self.index_outil_a_tateur = 0

        self.libelle_outil_a_tateur = self.font.render("OUTIL A TATEUR ", True, config.WHITE, config.BLACK)
        self.libelle_outil_a_tateurRect = self.libelle_outil_a_tateur.get_rect()
        self.libelle_outil_a_tateurRect.x = 10
        self.libelle_outil_a_tateurRect.y = 280

        self.btn_outil_a_tateur = self.font.render(self.list_outil_a_tateur[self.index_outil_a_tateur], True, config.GREEN, config.BLUE)
        self.btn_outil_a_tateurRect = self.btn_outil_a_tateur.get_rect()
        self.btn_outil_a_tateurRect.x = 260 + 140
        self.btn_outil_a_tateurRect.y = 280


        """
        self.btn_dec_outil_adaptable = self.font.render("<<:", True, config.YELLOW, config.GRAY)
        self.btn_dec_outil_adaptableRect = self.btn_dec_outil_adaptable.get_rect()
        self.btn_dec_outil_adaptableRect.x = 210 + 140
        self.btn_dec_outil_adaptableRect.y = 240

        self.btn_inc_outil_adaptable = self.font.render(":>>", True, config.YELLOW, config.GRAY)
        self.btn_inc_outil_adaptableRect = self.btn_inc_outil_adaptable.get_rect()
        self.btn_inc_outil_adaptableRect.x = 600 + 140
        self.btn_inc_outil_adaptableRect.y = 240
        """
        self.quel_champ = 0 # vise le champ que l'on est en train de rentrer
        self.nb_champ = 6    # nombre de champ que l'on peut saisir

        self.update()


    def update(self):

        if self.quel_champ == 0: #enter nom porteur
            self.btn_nom = self.font.render("|" + self.nom + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_nom = self.font.render("|" + self.nom + "|", True, config.YELLOW, config.GRAY)
        self.btn_nomRect = self.btn_nom.get_rect()
        self.btn_nomRect.x = 280
        self.btn_nomRect.y = 80

        if self.quel_champ == 1:
            self.btn_largeur_travail = self.font.render("|" + self.largeur_travail + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_largeur_travail = self.font.render("|" + self.largeur_travail + "|", True, config.YELLOW, config.GRAY)
        self.btn_largeur_travailRect = self.btn_largeur_travail.get_rect()
        self.btn_largeur_travailRect.x = 280 + 280
        self.btn_largeur_travailRect.y = 420

        if self.quel_champ == 2:
            self.btn_longueur_outil = self.font.render("|" + self.longueur_outil + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_longueur_outil = self.font.render("|" + self.longueur_outil + "|", True, config.YELLOW, config.GRAY)
        self.btn_longueur_outilRect = self.btn_longueur_outil.get_rect()
        self.btn_longueur_outilRect.x = 280 + 280
        self.btn_longueur_outilRect.y = 460

        if self.quel_champ == 3:
            self.btn_distance_gps_debut_outil = self.font.render("|" + self.distance_gps_debut_outil + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_distance_gps_debut_outil = self.font.render("|" + self.distance_gps_debut_outil+ "|", True, config.YELLOW, config.GRAY)
        self.btn_distance_gps_debut_outilRect = self.btn_distance_gps_debut_outil.get_rect()
        self.btn_distance_gps_debut_outilRect.x = 280 + 280
        self.btn_distance_gps_debut_outilRect.y = 500

        if self.quel_champ == 4:
            self.btn_distance_gps_exterieur_outil = self.font.render("|" + self.distance_gps_exterieur_outil + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_distance_gps_exterieur_outil = self.font.render("|" + self.distance_gps_exterieur_outil + "|", True, config.YELLOW, config.GRAY)
        self.btn_distance_gps_exterieur_outilRect = self.btn_distance_gps_exterieur_outil.get_rect()
        self.btn_distance_gps_exterieur_outilRect.x = 280 + 280
        self.btn_distance_gps_exterieur_outilRect.y = 540

        if self.quel_champ == 5:
            self.btn_penetration_in_intercep = self.font.render("|" + self.penetration_in_intercep + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_penetration_in_intercep = self.font.render("|" + self.penetration_in_intercep + "|", True, config.YELLOW, config.GRAY)
        self.btn_penetration_in_intercepYRect = self.btn_penetration_in_intercep.get_rect()
        self.btn_penetration_in_intercepRect.x = 280 + 280
        self.btn_penetration_in_intercepRect.y = 580

        """
        if self.quel_champ == 6:
            self.btn_hauteur_gps = self.font.render("|" + self.hauteur_gps + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_hauteur_gps = self.font.render("|" + self.hauteur_gps + "|", True, config.YELLOW, config.GRAY)
        self.btn_hauteur_gpsRect = self.btn_hauteur_gps.get_rect()
        self.btn_hauteur_gpsRect.x = 280
        self.btn_hauteur_gpsRect.y = 620

        if self.quel_champ == 7:
            self.btn_vitesse_max = self.font.render("|" + self.vitesse_max + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_vitesse_max = self.font.render("|" + self.vitesse_max + "|", True, config.YELLOW, config.GRAY)
        self.btn_vitesse_maxRect = self.btn_vitesse_max.get_rect()
        self.btn_vitesse_maxRect.x = 280
        self.btn_vitesse_maxRect.y = 660
        """

        self.type = self.font.render(self.list_type[self.index_type], True, config.GREEN, config.BLUE)
        self.typeRect = self.type.get_rect()
        self.typeRect.x = 260 + 100
        self.typeRect.y = 120

        self.partie_travaille  = self.font.render(self.list_partie_travaille [self.index_partie_travaille ], True, config.GREEN, config.BLUE)
        self.partie_travailleRect = self.partie_travaille .get_rect()
        self.partie_travailleRect.x = 260 + 100
        self.partie_travailleRect.y = 160

        if self.index_relevage == 0:
            self.btn_relevage = self.font.render(self.list_relevage[self.index_relevage], True, config.YELLOW, config.GRAY)
        else:
            self.btn_relevage = self.font.render(self.list_relevage[self.index_relevage], True, config.YELLOW, config.RED)
        self.btn_relevageRect = self.btn_relevage.get_rect()
        self.btn_relevageRect.x = 260 + 140
        self.btn_relevageRect.y = 200

        if self.index_action_au_cep == 0:
            self.btn_action_au_cep = self.font.render(self.list_action_au_cep[self.index_action_au_cep], True, config.YELLOW, config.GRAY)
        else:
            self.btn_action_au_cep = self.font.render(self.list_action_au_cep[self.index_action_au_cep], True, config.YELLOW, config.RED)
        self.btn_action_au_cepRect = self.btn_action_au_cep.get_rect()
        self.btn_action_au_cepRect.x = 260 + 140
        self.btn_action_au_cepRect.y = 240

        if self.index_outil_a_tateur == 0:
             self.btn_outil_a_tateur = self.font.render(self.list_outil_a_tateur[self.index_outil_a_tateur], True, config.YELLOW, config.GRAY)
        else:
            self.btn_outil_a_tateur = self.font.render(self.list_outil_a_tateur[self.index_outil_a_tateur], True, config.YELLOW, config.RED)
        self.btn_outil_a_tateurRect = self.btn_outil_a_tateur.get_rect()
        self.btn_outil_a_tateurRect.x = 260 + 140
        self.btn_outil_a_tateurRect.y = 280

        self.screen.blit(self.libelle_nom, self.libelle_nomRect)
        self.screen.blit(self.btn_nom, self.btn_nomRect)
        self.screen.blit(self.libelle_largeur_travail, self.libelle_largeur_travailRect)
        self.screen.blit(self.btn_largeur_travail, self.btn_largeur_travailRect)
        self.screen.blit(self.libelle_longeur_outil, self.libelle_longeur_outilRect)
        self.screen.blit(self.btn_longueur_outil, self.btn_longueur_outilRect)
        self.screen.blit(self.libelle_distance_gps_debut_outil, self.libelle_distance_gps_debut_outilRect)
        self.screen.blit(self.btn_distance_gps_debut_outil, self.btn_distance_gps_debut_outilRect)
        self.screen.blit(self.libelle_distance_gps_exterieur_outil, self.libelle_distance_gps_exterieur_outilRect)
        self.screen.blit(self.btn_distance_gps_exterieur_outil, self.btn_distance_gps_exterieur_outilRect)
        self.screen.blit(self.libelle_penetration_in_intercep, self.libelle_penetration_in_intercepRect)
        self.screen.blit(self.btn_penetration_in_intercep, self.btn_penetration_in_intercepRect)
        #self.screen.blit(self.libelle_hauteur_antene_gps, self.libelle_hauteur_antene_gpsRect)
        #self.screen.blit(self.btn_hauteur_gps, self.btn_hauteur_gpsRect)
        #self.screen.blit(self.libelle_vitesse_max, self.libelle_vitesse_maxRect)
        #self.screen.blit(self.btn_vitesse_max, self.btn_vitesse_maxRect)
        self.screen.blit(self.libelle_type, self.libelle_typeRect)
        self.screen.blit(self.type, self.typeRect)
        self.screen.blit(self.btn_dec_type, self.btn_dec_typeRect)
        self.screen.blit(self.btn_inc_type, self.btn_inc_typeRect)
        self.screen.blit(self.libelle_partie_travaille , self.libelle_partie_travailleRect)
        self.screen.blit(self.partie_travaille , self.partie_travailleRect)
        self.screen.blit(self.btn_dec_partie_travaille , self.btn_dec_partie_travailleRect)
        self.screen.blit(self.btn_inc_partie_travaille , self.btn_inc_partie_travailleRect)
        self.screen.blit(self.libelle_relevage, self.libelle_relevageRect)
        self.screen.blit(self.btn_relevage, self.btn_relevageRect)
        self.screen.blit(self.libelle_outil_a_tateur,self.libelle_outil_a_tateurRect)
        self.screen.blit(self.btn_outil_a_tateur,self.btn_outil_a_tateurRect)
        #self.screen.blit(self.btn_dec_choix_outil, self.btn_dec_choix_outilRect)
        #self.screen.blit(self.btn_inc_choix_outil, self.btn_inc_choix_outilRect)

        self.screen.blit(self.libelle_action_au_cep, self.libelle_action_au_cepRect)
        self.screen.blit(self.btn_action_au_cep, self.btn_action_au_cepRect)
        #self.screen.blit(self.btn_dec_outil_adaptable, self.btn_dec_outil_adaptableRect)
        #self.screen.blit(self.btn_inc_outil_adaptable, self.btn_inc_outil_adaptableRect)


    def enter_text(self,chaine, caractere, longueur):
        # le code ascii de backspace est 8 ord(caractere) supp = 127 = ord(caractere) print(ord(caractere))
        if len(caractere) != 1: # permet d'eviter de prendre autre chose que les chiffre et charactere
            caractere = "/"
        
        if ord(caractere) == 8 or ord(caractere) == 127: # traite backspace et suppr
            chaine = chaine[0:-1]
        elif 94 < ord(caractere) < 123 or 64 < ord(caractere) < 91 or 47 < ord(caractere) < 58: # accepte les lettre et les chiffre 
            chaine = chaine + caractere
        if len(chaine) > longueur:
            chaine = chaine[0:-1]
        return chaine
    
    def enter_nombre(self, chaine, caractere):
        if len(caractere) != 1: # permet d'eviter de prendre autre chose que les chiffre et charactere
            caractere = "/"
        if ord(caractere) == 46 and chaine.find(".") > -1: # permet de ne pas doubler le . point
            caractere = "/"
        if ord(caractere) == 8 or ord(caractere) == 127:# traite backspace et suppr
                chaine = chaine[0:-1]
        if 47 < ord(caractere) < 58 or ord(caractere) == 46:  # accepte les chiffre et le point
            chaine = chaine + caractere
        return chaine

    def gestion(self):
        gs = main.GpsPoller()
        gs.start() # start it up

        titre = "**EasyVine CREAT PORTEUR **  " # + format(self.latitude, '.7f') + "   long: " + format(self.longitude, '.7f') + "  track: " + format(self.track,'.2f')  # + "  altitude: " + format(self.altitude, '.4f')
        pygame.display.set_caption(titre)
        while True:

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
                
                elif event.type == pygame.KEYDOWN: # KEYDOWN
                    recup_commande = pygame.key.name(event.key)
                    if recup_commande == "return" or recup_commande == "tab" or recup_commande == "enter": # tab =acsii 9  return = ascii 13
                        self.quel_champ +=1
                        if self.quel_champ == self.nb_champ:
                            self.quel_champ = 0
                        
                    if self.quel_champ == 0: #enter nom porteur
                        self.nom = self.enter_text(self.nom, event.unicode, 20)
                    elif self.quel_champ == 1:  # entre voie du porteur
                        self.largeur_travail = self.enter_nombre(self.largeur_travail, event.unicode)
                    elif self.quel_champ == 2:
                        self.longueur_outil = self.enter_nombre(self.longueur_outil, event.unicode)
                    if self.quel_champ == 3:
                        self.distance_gps_debut_outil = self.enter_nombre(self.distance_gps_debut_outil, event.unicode)
                    if self.quel_champ == 4:
                        self.distance_gps_exterieur_outil = self.enter_nombre(self.distance_gps_exterieur_outil, event.unicode)
                    if self.quel_champ == 5:
                        self.penetration_in_intercep = self.enter_nombre(self.penetration_in_intercep, event.unicode)
                    if self.quel_champ == 6:
                        self.hauteur_gps = self.enter_nombre(self.hauteur_gps, event.unicode)
                    if self.quel_champ == 7:
                        self.vitesse_max = self.enter_nombre(self.vitesse_max, event.unicode)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_nomRect.collidepoint(event.pos):
                        self.quel_champ = 0  
                    elif self.btn_largeur_travailRect.collidepoint(event.pos):
                        self.quel_champ = 1
                    elif self.btn_longueur_outilRect.collidepoint(event.pos):
                        self.quel_champ = 2
                    elif self.btn_distance_gps_debut_outilRect.collidepoint(event.pos):
                        self.quel_champ = 3
                    elif self.btn_distance_gps_exterieur_outilRect.collidepoint(event.pos):
                        self.quel_champ = 4
                    elif self.btn_penetration_in_intercepRect.collidepoint(event.pos):
                        self.quel_champ = 5
                        
                    #elif self.btn_hauteur_gpsRect.collidepoint(event.pos):
                    #    self.quel_champ = 6
                    #elif self.btn_vitesse_maxRect.collidepoint(event.pos):
                    #    self.quel_champ = 7

                    elif self.btn_inc_typeRect.collidepoint(event.pos):
                        self.index_type +=1
                        if self.index_type == len(self.list_type):
                            self.index_type = 0

                    elif self.btn_dec_typeRect.collidepoint(event.pos):
                        self.index_type -= 1
                        if self.index_type < 0:
                            self.index_type = len(self.list_type) - 1

                    elif self.btn_dec_partie_travailleRect.collidepoint(event.pos):
                        self.index_partie_travaille += 1
                        if self.index_partie_travaille == len(self.list_partie_travaille):
                            self.index_partie_travaille = 0

                    elif self.btn_inc_partie_travailleRect.collidepoint(event.pos):
                        self.index_partie_travaille -= 1
                        if self.index_partie_travaille < 0 :
                            self.index_partie_travaille = len(self.list_partie_travaille) -1

                    elif self.btn_relevageRect.collidepoint(event.pos):
                        self.index_relevage += 1
                        if self.index_relevage > 1:
                            self.index_relevage = 0
                            
                    elif self.btn_action_au_cepRect.collidepoint(event.pos):
                        self.index_action_au_cep += 1
                        if self.index_action_au_cep > 1:
                            self.index_action_au_cep = 0

                    elif self.btn_outil_a_tateurRect.collidepoint(event.pos):
                        self.index_outil_a_tateur += 1
                        if self.index_outil_a_tateur > 1:
                            self.index_outil_a_tateur = 0


                    

                    

                   

                    ########## ON RETURN AU FICHIER windowscan POUR CHANGER DE MODULE ###########
                    elif self.module.buton_gRect.collidepoint(event.pos):
                        return -1 # on return au fichier windowscan.py pour changer de module
                    elif self.module.buton_dRect.collidepoint(event.pos):
                        return 1  # on return au fichier windowscan.py pour changer de module

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
                    if retour == 0 : # si l'ACTION change return a windowscan et return a main.py 
                        return 0