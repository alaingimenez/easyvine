# windowcreatporteur



import config
import main


import pygame
pygame.init()







class WindowCreatPorteur:
    def __init__(self, window_m, module, parcel):

        self.window_main = window_m
        self.screen = self.window_main.screen
        self.module = module
        self.parcel = parcel
        self.main = main.Main()
        
        

        self.parcel = self.window_main.fichier.load_parcelle(self.window_main.name_parcelle) # comment on charge un objet

        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_g = pygame.font.Font('freesansbold.ttf', 80)

        self.libelle_porteur = self.font.render("Nom du Porteur", True, config.WHITE, config.BLACK)
        self.libelle_porteurRect = self.libelle_porteur.get_rect()
        self.libelle_porteurRect.x = 10
        self.libelle_porteurRect.y = 80 

        self.nom =""
        self.btn_nom = self.font.render("|" + self.nom + "|", True, config.YELLOW, config.GRAY)
        self.btn_nomRect = self.btn_nom.get_rect()
        self.btn_nomRect.x = 280
        self.btn_nomRect.y = 80

        self.libelle_voie = self.font.render("Voie : ", True, config.WHITE, config.BLACK)
        self.libelle_voieRect = self.libelle_voie.get_rect()
        self.libelle_voieRect.x = 10
        self.libelle_voieRect.y = 120

        self.voie = ""
        self.btn_voie = self.font.render("|" + self.voie + "|", True, config.YELLOW, config.GRAY)
        self.btn_voieRect = self.btn_voie.get_rect()
        self.btn_voieRect.x = 280
        self.btn_voieRect.y = 120

        self.libelle_empattement = self.font.render("Empattement : ", True, config.WHITE, config.BLACK)
        self.libelle_empattementRect = self.libelle_empattement.get_rect()
        self.libelle_empattementRect.x = 10
        self.libelle_empattementRect.y = 160

        self.empattement = ""
        self.btn_empattement = self.font.render("|" + self.empattement + "|", True, config.YELLOW, config.GRAY)
        self.btn_empattementRect = self.btn_empattement.get_rect()
        self.btn_empattementRect.x = 280
        self.btn_empattementRect.y = 160

        self.libelle_rayon_braquage = self.font.render("Rayon Braquage : ", True, config.WHITE, config.BLACK)
        self.libelle_rayon_braquageRect = self.libelle_rayon_braquage.get_rect()
        self.libelle_rayon_braquageRect.x = 10
        self.libelle_rayon_braquageRect.y = 200

        self.rayon_braquage =""
        self.btn_rayon_braquage = self.font.render("|" + self.rayon_braquage+ "|", True, config.YELLOW, config.GRAY)
        self.btn_rayon_braquageRect = self.btn_rayon_braquage.get_rect()
        self.btn_rayon_braquageRect.x = 280
        self.btn_rayon_braquageRect.y = 200

        self.libelle_position_antene_gpsX = self.font.render("Position GPS X: ", True, config.WHITE, config.BLACK)
        self.libelle_position_antene_gpsXRect = self.libelle_position_antene_gpsX.get_rect()
        self.libelle_position_antene_gpsXRect.x = 10
        self.libelle_position_antene_gpsXRect.y = 240

        self.pos_gpsX = ""
        self.btn_pos_gpsX = self.font.render("|" + self.pos_gpsX + "|", True, config.YELLOW, config.GRAY)
        self.btn_pos_gpsXRect = self.btn_pos_gpsX.get_rect()
        self.btn_pos_gpsXRect.x = 280
        self.btn_pos_gpsXRect.y = 240

        self.libelle_position_antene_gpsY = self.font.render("Position GPS Y: ", True, config.WHITE, config.BLACK)
        self.libelle_position_antene_gpsYRect = self.libelle_position_antene_gpsY.get_rect()
        self.libelle_position_antene_gpsYRect.x = 10
        self.libelle_position_antene_gpsYRect.y = 280

        self.pos_gpsY = ""
        self.btn_pos_gpsY = self.font.render("|" + self.pos_gpsY + "|", True, config.YELLOW, config.GRAY)
        self.btn_pos_gpsYRect = self.btn_pos_gpsY.get_rect()
        self.btn_pos_gpsYRect.x = 280
        self.btn_pos_gpsYRect.y = 280

        self.libelle_hauteur_antene_gps = self.font.render("Hauteur GPS: ", True, config.WHITE, config.BLACK)
        self.libelle_hauteur_antene_gpsRect = self.libelle_hauteur_antene_gps.get_rect()
        self.libelle_hauteur_antene_gpsRect.x = 10
        self.libelle_hauteur_antene_gpsRect.y = 320

        self.hauteur_gps = ""
        self.btn_hauteur_gps = self.font.render("|" + self.hauteur_gps + "|", True, config.YELLOW, config.GRAY)
        self.btn_hauteur_gpsRect = self.btn_hauteur_gps.get_rect()
        self.btn_hauteur_gpsRect.x = 280
        self.btn_hauteur_gpsRect.y = 320
       
        self.libelle_vitesse_max = self.font.render("Vitesse Max: ", True, config.WHITE, config.BLACK)
        self.libelle_vitesse_maxRect = self.libelle_vitesse_max.get_rect()
        self.libelle_vitesse_maxRect.x = 10
        self.libelle_vitesse_maxRect.y = 360

        self.vitesse_max = ""
        self.btn_vitesse_max = self.font.render("|" + self.vitesse_max + "|", True, config.YELLOW, config.GRAY)
        self.btn_vitesse_maxRect = self.btn_vitesse_max.get_rect()
        self.btn_vitesse_maxRect.x = 280
        self.btn_vitesse_maxRect.y = 360

        self.list_type = config.LIST_TYPE_TRACTEUR
        self.index_type = 0
        

        self.libelle_type= self.font.render("TYPE: ", True, config.WHITE, config.BLACK)
        self.libelle_typeRect = self.libelle_type.get_rect()
        self.libelle_typeRect.x = 10
        self.libelle_typeRect.y = 420

        self.type = self.font.render(self.list_type[self.index_type], True, config.GREEN, config.BLUE)
        self.typeRect = self.type.get_rect()
        self.typeRect.x = 260
        self.typeRect.y = 420

        self.btn_dec_type = self.font.render("<<:", True, config.YELLOW, config.GRAY)
        self.btn_dec_typeRect = self.btn_dec_type.get_rect()
        self.btn_dec_typeRect.x = 210
        self.btn_dec_typeRect.y = 420

        self.btn_inc_type = self.font.render(":>>", True, config.YELLOW, config.GRAY)
        self.btn_inc_typeRect = self.btn_inc_type.get_rect()
        self.btn_inc_typeRect.x = 670
        self.btn_inc_typeRect.y = 420

        self.list_direction = config.LIST_DIRECTION_TRACTEUR
        self.index_direction = 0
        

        self.libelle_direction = self.font.render("DIRECTION: ", True, config.WHITE, config.BLACK)
        self.libelle_directionRect = self.libelle_direction.get_rect()
        self.libelle_directionRect.x = 10
        self.libelle_directionRect.y = 460

        self.direction = self.font.render(self.list_direction[self.index_direction], True, config.GREEN, config.BLUE)
        self.directionRect = self.direction.get_rect()
        self.directionRect.x = 260
        self.directionRect.y = 460

        self.btn_dec_direction = self.font.render("<<:", True, config.YELLOW, config.GRAY)
        self.btn_dec_directionRect = self.btn_dec_direction.get_rect()
        self.btn_dec_directionRect.x = 210
        self.btn_dec_directionRect.y = 460

        self.btn_inc_direction = self.font.render(":>>", True, config.YELLOW, config.GRAY)
        self.btn_inc_directionRect = self.btn_inc_direction.get_rect()
        self.btn_inc_directionRect.x = 670
        self.btn_inc_directionRect.y = 460

        #self.list_choix_outils = [config.OUTIL_OBLIGATOIRE, "premier outil", "2eme outil"]
        self.index_choix_outil = 0
        

        self.libelle_choix_outil = self.font.render("BASE D'OUTILS: ", True, config.WHITE, config.BLACK)
        self.libelle_choix_outilRect = self.libelle_choix_outil.get_rect()
        self.libelle_choix_outilRect.x = 10
        self.libelle_choix_outilRect.y = 540

        self.choix_outil = self.font.render(self.main.list_outil[self.index_choix_outil], True, config.GREEN, config.BLUE)
        self.choix_outilRect = self.choix_outil.get_rect()
        self.choix_outilRect.x = 260 + 140
        self.choix_outilRect.y = 540

        self.btn_dec_choix_outil= self.font.render("<<:", True, config.YELLOW, config.GRAY)
        self.btn_dec_choix_outilRect = self.btn_dec_choix_outil.get_rect()
        self.btn_dec_choix_outilRect.x = 210 + 140
        self.btn_dec_choix_outilRect.y = 540

        self.btn_inc_choix_outil = self.font.render(":>>", True, config.YELLOW, config.GRAY)
        self.btn_inc_choix_outilRect = self.btn_inc_choix_outil.get_rect()
        self.btn_inc_choix_outilRect.x = 600 + 140
        self.btn_inc_choix_outilRect.y = 540

        self.btn_add_outil = self.font.render("v ADDS v",True, config.YELLOW, config.GRAY)
        self.btn_add_outilRect = self.btn_add_outil.get_rect()
        self.btn_add_outilRect.x = 280 + 100
        self.btn_add_outilRect.y = 590 

        self.btn_remove_outil = self.font.render("^ REMOVE ^",True, config.YELLOW, config.GRAY)
        self.btn_remove_outilRect = self.btn_remove_outil.get_rect()
        self.btn_remove_outilRect.x = 480 + 100
        self.btn_remove_outilRect.y = 590

        self.list_outils_adaptable = [config.OUTIL_OBLIGATOIRE]
        self.index_outil_adaptable = 0
        

        self.libelle_outil_adaptable = self.font.render("OUTILS ADAPTABLE : ", True, config.WHITE, config.BLACK)
        self.libelle_outil_adaptableRect = self.libelle_outil_adaptable.get_rect()
        self.libelle_outil_adaptableRect.x = 10
        self.libelle_outil_adaptableRect.y = 640

        self.outil_adaptable = self.font.render(self.list_outils_adaptable[self.index_outil_adaptable], True, config.GREEN, config.BLUE)
        self.outil_adaptableRect = self.outil_adaptable.get_rect()
        self.outil_adaptableRect.x = 260 + 140
        self.outil_adaptableRect.y = 640

        self.btn_dec_outil_adaptable = self.font.render("<<:", True, config.YELLOW, config.GRAY)
        self.btn_dec_outil_adaptableRect = self.btn_dec_outil_adaptable.get_rect()
        self.btn_dec_outil_adaptableRect.x = 210 + 140
        self.btn_dec_outil_adaptableRect.y = 640

        self.btn_inc_outil_adaptable = self.font.render(":>>", True, config.YELLOW, config.GRAY)
        self.btn_inc_outil_adaptableRect = self.btn_inc_outil_adaptable.get_rect()
        self.btn_inc_outil_adaptableRect.x = 600 + 140
        self.btn_inc_outil_adaptableRect.y = 640

        self.quel_champ = 0 # vise le champ que l'on est en train de rentrer
        self.nb_champ = 8    # nombre de champ que l'on peut saisir



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
            self.btn_voie = self.font.render("|" + self.voie + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_voie = self.font.render("|" + self.voie + "|", True, config.YELLOW, config.GRAY)
        self.btn_voieRect = self.btn_voie.get_rect()
        self.btn_voieRect.x = 280
        self.btn_voieRect.y = 120

        if self.quel_champ == 2:
            self.btn_empattement = self.font.render("|" + self.empattement + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_empattement = self.font.render("|" + self.empattement + "|", True, config.YELLOW, config.GRAY)
        self.btn_empattementRect = self.btn_empattement.get_rect()
        self.btn_empattementRect.x = 280
        self.btn_empattementRect.y = 160

        if self.quel_champ == 3:
            self.btn_rayon_braquage = self.font.render("|" + self.rayon_braquage+ "|", True, config.YELLOW, config.RED)
        else:
            self.btn_rayon_braquage = self.font.render("|" + self.rayon_braquage+ "|", True, config.YELLOW, config.GRAY)
        self.btn_rayon_braquageRect = self.btn_rayon_braquage.get_rect()
        self.btn_rayon_braquageRect.x = 280
        self.btn_rayon_braquageRect.y = 200

        if self.quel_champ == 4:
            self.btn_pos_gpsX = self.font.render("|" + self.pos_gpsX + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_pos_gpsX = self.font.render("|" + self.pos_gpsX + "|", True, config.YELLOW, config.GRAY)
        self.btn_pos_gpsXRect = self.btn_pos_gpsX.get_rect()
        self.btn_pos_gpsXRect.x = 280
        self.btn_pos_gpsXRect.y = 240

        if self.quel_champ == 5:
            self.btn_pos_gpsY = self.font.render("|" + self.pos_gpsY + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_pos_gpsY = self.font.render("|" + self.pos_gpsY + "|", True, config.YELLOW, config.GRAY)
        self.btn_pos_gpsYRect = self.btn_pos_gpsY.get_rect()
        self.btn_pos_gpsYRect.x = 280
        self.btn_pos_gpsYRect.y = 280

        if self.quel_champ == 6:
            self.btn_hauteur_gps = self.font.render("|" + self.hauteur_gps + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_hauteur_gps = self.font.render("|" + self.hauteur_gps + "|", True, config.YELLOW, config.GRAY)
        self.btn_hauteur_gpsRect = self.btn_hauteur_gps.get_rect()
        self.btn_hauteur_gpsRect.x = 280
        self.btn_hauteur_gpsRect.y = 320

        if self.quel_champ == 7:
            self.btn_vitesse_max = self.font.render("|" + self.vitesse_max + "|", True, config.YELLOW, config.RED)
        else:
            self.btn_vitesse_max = self.font.render("|" + self.vitesse_max + "|", True, config.YELLOW, config.GRAY)
        self.btn_vitesse_maxRect = self.btn_vitesse_max.get_rect()
        self.btn_vitesse_maxRect.x = 280
        self.btn_vitesse_maxRect.y = 360
   
        self.type = self.font.render(self.list_type[self.index_type], True, config.GREEN, config.BLUE)
        self.typeRect = self.type.get_rect()
        self.typeRect.x = 260
        self.typeRect.y = 420

        self.direction = self.font.render(self.list_direction[self.index_direction], True, config.GREEN, config.BLUE)
        self.directionRect = self.direction.get_rect()
        self.directionRect.x = 260
        self.directionRect.y = 460

        
        self.choix_outil = self.font.render(self.main.list_outil[self.index_choix_outil], True, config.GREEN, config.BLUE)
        self.choix_outilRect = self.choix_outil.get_rect()
        self.choix_outilRect.x = 260 + 140
        self.choix_outilRect.y = 540

        self.outil_adaptable = self.font.render(self.list_outils_adaptable[self.index_outil_adaptable], True, config.GREEN, config.BLUE)
        self.outil_adaptableRect = self.outil_adaptable.get_rect()
        self.outil_adaptableRect.x = 260 + 140
        self.outil_adaptableRect.y = 640
        
        

        self.screen.blit(self.libelle_porteur, self.libelle_porteurRect)
        self.screen.blit(self.btn_nom, self.btn_nomRect)
        self.screen.blit(self.libelle_voie, self.libelle_voieRect)
        self.screen.blit(self.btn_voie, self.btn_voieRect)
        self.screen.blit(self.libelle_empattement, self.libelle_empattementRect)
        self.screen.blit(self.btn_empattement, self.btn_empattementRect)
        self.screen.blit(self.libelle_rayon_braquage, self.libelle_rayon_braquageRect)
        self.screen.blit(self.btn_rayon_braquage, self.btn_rayon_braquageRect)
        self.screen.blit(self.libelle_position_antene_gpsX, self.libelle_position_antene_gpsXRect)
        self.screen.blit(self.btn_pos_gpsX, self.btn_pos_gpsXRect)
        self.screen.blit(self.libelle_position_antene_gpsY, self.libelle_position_antene_gpsYRect)
        self.screen.blit(self.btn_pos_gpsY, self.btn_pos_gpsYRect)
        self.screen.blit(self.libelle_hauteur_antene_gps, self.libelle_hauteur_antene_gpsRect)
        self.screen.blit(self.btn_hauteur_gps, self.btn_hauteur_gpsRect)
        self.screen.blit(self.libelle_vitesse_max, self.libelle_vitesse_maxRect)
        self.screen.blit(self.btn_vitesse_max, self.btn_vitesse_maxRect)
        self.screen.blit(self.libelle_type, self.libelle_typeRect)
        self.screen.blit(self.type, self.typeRect)
        self.screen.blit(self.btn_dec_type, self.btn_dec_typeRect)
        self.screen.blit(self.btn_inc_type, self.btn_inc_typeRect)
        self.screen.blit(self.libelle_direction, self.libelle_directionRect)
        self.screen.blit(self.direction, self.directionRect)
        self.screen.blit(self.btn_dec_direction, self.btn_dec_directionRect)
        self.screen.blit(self.btn_inc_direction, self.btn_inc_directionRect)
        self.screen.blit(self.libelle_choix_outil, self.libelle_choix_outilRect)
        self.screen.blit(self.choix_outil, self.choix_outilRect)
        self.screen.blit(self.btn_dec_choix_outil, self.btn_dec_choix_outilRect)
        self.screen.blit(self.btn_inc_choix_outil, self.btn_inc_choix_outilRect)
        self.screen.blit(self.btn_add_outil, self.btn_add_outilRect)
        self.screen.blit(self.btn_remove_outil, self.btn_remove_outilRect)
        self.screen.blit(self.libelle_outil_adaptable, self.libelle_outil_adaptableRect)
        self.screen.blit(self.outil_adaptable, self.outil_adaptableRect)
        self.screen.blit(self.btn_dec_outil_adaptable, self.btn_dec_outil_adaptableRect)
        self.screen.blit(self.btn_inc_outil_adaptable, self.btn_inc_outil_adaptableRect)


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
                        self.voie = self.enter_nombre(self.voie, event.unicode)
                    elif self.quel_champ == 2:
                        self.empattement = self.enter_nombre(self.empattement, event.unicode)
                    if self.quel_champ == 3:
                        self.rayon_braquage = self.enter_nombre(self.rayon_braquage, event.unicode)
                    if self.quel_champ == 4:
                        self.pos_gpsX = self.enter_nombre(self.pos_gpsX, event.unicode)
                    if self.quel_champ == 5:
                        self.pos_gpsY = self.enter_nombre(self.pos_gpsY, event.unicode)
                    if self.quel_champ == 6:
                        self.hauteur_gps = self.enter_nombre(self.hauteur_gps, event.unicode)
                    if self.quel_champ == 7:
                        self.vitesse_max = self.enter_nombre(self.vitesse_max, event.unicode)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_nomRect.collidepoint(event.pos):
                        self.quel_champ = 0  
                    elif self.btn_voieRect.collidepoint(event.pos):
                        self.quel_champ = 1
                    elif self.btn_empattementRect.collidepoint(event.pos):
                        self.quel_champ = 2
                    elif self.btn_rayon_braquageRect.collidepoint(event.pos):
                        self.quel_champ = 3
                    elif self.btn_pos_gpsXRect.collidepoint(event.pos):
                        self.quel_champ = 4
                    elif self.btn_pos_gpsYRect.collidepoint(event.pos):
                        self.quel_champ = 5
                    elif self.btn_hauteur_gpsRect.collidepoint(event.pos):
                        self.quel_champ = 6
                    elif self.btn_vitesse_maxRect.collidepoint(event.pos):
                        self.quel_champ = 7

                    elif self.btn_inc_typeRect.collidepoint(event.pos):
                        self.index_type +=1
                        if self.index_type == len(self.list_type):
                            self.index_type = 0

                    elif self.btn_dec_typeRect.collidepoint(event.pos):
                        self.index_type -= 1
                        if self.index_type < 0:
                            self.index_type = len(self.list_type) - 1

                    elif self.btn_dec_directionRect.collidepoint(event.pos):
                        self.index_direction += 1
                        if self.index_direction == len(self.list_direction):
                            self.index_direction = 0

                    elif self.btn_inc_directionRect.collidepoint(event.pos):
                        self.index_direction -= 1
                        if self.index_direction < 0 :
                            self.index_direction = len(self.list_direction) -1

                    elif self.btn_dec_choix_outilRect.collidepoint(event.pos):
                        self.index_choix_outil -= 1
                        if self.index_choix_outil < 0:
                            self.index_choix_outil = len(self.main.list_outil) - 1

                    elif self.btn_inc_choix_outilRect.collidepoint(event.pos):
                        self.index_choix_outil += 1
                        if self.index_choix_outil == len(self.main.list_outil):
                            self.index_choix_outil = 0

                    elif self.btn_dec_outil_adaptableRect.collidepoint(event.pos):
                        self.index_outil_adaptable -= 1
                        if self.index_outil_adaptable < 0:
                            self.index_outil_adaptable = len(self.list_outils_adaptable) - 1

                    elif self.btn_inc_outil_adaptableRect.collidepoint(event.pos):
                        self.index_outil_adaptable += 1
                        if self.index_outil_adaptable == len(self.list_outils_adaptable):
                            self.index_outil_adaptable = 0

                    elif self.btn_add_outilRect.collidepoint(event.pos):
                        if (self.list_outils_adaptable.count(self.main.list_outil[self.index_choix_outil])) < 1: # on peut ajouter l'outil que si il n'y ai pas
                            self.list_outils_adaptable.append(self.main.list_outil[self.index_choix_outil])
                            self.index_outil_adaptable = len(self.list_outils_adaptable)-1

                    elif self.btn_remove_outilRect.collidepoint(event.pos):
                        if config.OUTIL_OBLIGATOIRE != self.list_outils_adaptable[self.index_outil_adaptable]: # empeche d'enlever l'outil obigatoire
                            del self.list_outils_adaptable[self.index_outil_adaptable]
                            if len(self.list_outils_adaptable) <= self.index_outil_adaptable:
                                self.index_outil_adaptable = len(self.list_outils_adaptable)-1

                    ########## ON RETURN AU FICHIER windowscan POUR CHANGER DE MODULE ###########
                    elif self.module.buton_gRect.collidepoint(event.pos):
                        del self.main
                        return -1 # on return au fichier windowscan.py pour changer de module
                    elif self.module.buton_dRect.collidepoint(event.pos):
                        del self.main
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
                        del self.main
                        return 0