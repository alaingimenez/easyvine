import pickle
import time
import parcelle
import windowfichierdelete
import main
import pygame

pygame.init()

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)


TIME_MSG = 1



class WindowFichierCreate:
    def __init__(self, screen, fichier, window_main):

        self.window_main = window_main

        self.fichier = fichier # recuperer l'objet fichier qui permet d'avoir acces au sauvegarde et a la liste des fichier

        self.parcel = parcelle.Parcelle()
        #self.new_parcel = parcelle.NewParcelle()

        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf',30)
        self.font_un = pygame.font.Font('freesansbold.ttf', 50)

        self.titre_window = "Fichier cretat"
        self.decalage_heigh = 100

        self.libelle_nom = self.font.render("Nom  Vigne : ", True, WHITE, BLACK)
        self.libelle_nomRect = self.libelle_nom.get_rect()
        self.libelle_nomRect.x = 10
        self.libelle_nomRect.y = 50 + self.decalage_heigh

        self.libelle_largeur_rang = self.font.render("Largeur rang : ", True, WHITE, BLACK)
        self.libelle_largeur_rangRect = self.libelle_largeur_rang.get_rect()
        self.libelle_largeur_rangRect.x = 10
        self.libelle_largeur_rangRect.y = 90 + self.decalage_heigh

        self.libelle_distance_souche = self.font.render("Distance souche : ", True, WHITE, BLACK)
        self.libelle_distance_soucheRect = self.libelle_distance_souche.get_rect()
        self.libelle_distance_soucheRect.x = 10
        self.libelle_distance_soucheRect.y = 130 + self.decalage_heigh

        self.libelle_cepage = self.font.render("   Cepage : ", True, WHITE, BLACK)
        self.libelle_cepageRect = self.libelle_cepage.get_rect()
        self.libelle_cepageRect.x = 10
        self.libelle_cepageRect.y = 170 + self.decalage_heigh

        self.buton_save = self.font_un.render("| SAVE |", True, YELLOW, GRAY)
        self.buton_saveRect = self.buton_save.get_rect()
        self.buton_saveRect.x = 800  #width
        self.buton_saveRect.y = 70 #height

        self.buton_trans = self.font_un.render("|transforme|", True, RED, GRAY)
        self.buton_transRect = self.buton_trans.get_rect()
        self.buton_transRect.x = 600  #width
        self.buton_transRect.y = 800 #height

        self.libelle_saving = self.font_un.render("** SAVING **", True, GREEN, GRAY)
        self.libelle_savingRect = self.libelle_saving.get_rect()
        self.libelle_savingRect.x = 600
        self.libelle_savingRect.y = 300

        self.quel_info = 0
        self.name = ""
        self.largeur_rang = ""
        self.distance_souche = ""
        self.cepage = ""

        self.chang_info()


        self.init()

    def init(self):
        pygame.display.set_caption(self.titre_window)

        #pygame.Surface.fill(self.screen, BLACK)

        self.screen.blit(self.libelle_nom, self.libelle_nomRect)
        self.screen.blit(self.libelle_largeur_rang, self.libelle_largeur_rangRect)
        self.screen.blit(self.libelle_distance_souche, self.libelle_distance_soucheRect)
        self.screen.blit(self.libelle_cepage, self.libelle_cepageRect)
        self.screen.blit(self.bouton_nom, self.bouton_nomRect)
        self.screen.blit(self.bouton_largeur_rang, self.bouton_largeur_rangRect)
        self.screen.blit(self.bouton_distance_souche, self.bouton_distance_soucheRect)
        self.screen.blit(self.bouton_cepage, self.bouton_cepageRect)
        self.screen.blit(self.buton_save, self.buton_saveRect)
        self.screen.blit(self.buton_trans, self.buton_transRect)


    def update(self, event):


        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.bouton_nomRect.collidepoint(event.pos):
                self.quel_info = 0  # print ("je rentre le nom de la vigne")
                self.chang_info()
            elif self.bouton_largeur_rangRect.collidepoint(event.pos):
                self.quel_info = 1  # print ("je rentre le nom de la vigne")
                self.chang_info()
            elif self.bouton_distance_soucheRect.collidepoint(event.pos):
                self.quel_info = 2  # print ("je rentre le nom de la vigne")
                self.chang_info()
            elif self.bouton_cepageRect.collidepoint(event.pos):
                self.quel_info = 3  # print ("je rentre le nom de la vigne")
                self.chang_info()
            elif self.buton_saveRect.collidepoint(event.pos):
                self.save()
            elif self.buton_transRect.collidepoint(event.pos):
                self.transforme()

        elif event.type == pygame.KEYDOWN: # KEYDOWN

            recup_commande = pygame.key.name(event.key) # permet de recuperer le commande  TAB  RETURN
            recup_touche = event.unicode # recupere la lettre ou le chiffre
            print("recup commande " + recup_commande)
            #print("recup touche  " + recup_touche)
            if recup_commande == "return" or recup_commande == "tab" or recup_commande == "enter": # tab =acsii9  return = ascii13
                self.quel_info +=1
                if self.quel_info == 4:
                    self.quel_info = 0
                self.chang_info()

            if len(recup_touche) != 1: # permet d'eviter de prendre autre chose que les chiffre et charactere
                recup_touche = "/"

            if self.quel_info == 0: # entre le name
                if 94 < ord(recup_touche) < 123 or 64 < ord(recup_touche) < 91 or 47 < ord(recup_touche) < 58:
                    self.name  = self.name + recup_touche
                if recup_commande == "backspace" or len(self.name) == 21:
                    self.name  = self.name [0:-1]
            elif self.quel_info == 1: # largeur du rang
                sortir_point = False
                if ord(recup_touche) == 46 and self.largeur_rang.find(".") > -1:
                    sortir_point = True
                if 47 < ord(recup_touche) < 58 or ord(recup_touche) == 46:
                    self.largeur_rang = self.largeur_rang + recup_touche
                if recup_commande == "backspace" or sortir_point:  # bakspace ou si on a ajouter un deuxieme point on le retire
                    self.largeur_rang = self.largeur_rang[0:-1]
            elif self.quel_info == 2: # distance souche
                sortir_point = False
                if ord(recup_touche) == 46 and self.distance_souche.find(".") > -1:
                    sortir_point = True
                if 47 < ord(recup_touche) < 58 or ord(recup_touche) == 46:
                    self.distance_souche = self.distance_souche + recup_touche
                if recup_commande == "backspace" or sortir_point:  # bakspace ou si on a ajouter un deuxieme point on le retire
                    self.distance_souche = self.distance_souche[0:-1]
            elif self.quel_info == 3: # cepage
                if 94 < ord(recup_touche) < 123 or 64 < ord(recup_touche) < 91 or 47 < ord(recup_touche) < 58:
                    self.cepage  = self.cepage  + recup_touche
                if recup_commande == "backspace" or len(self.cepage ) == 21:
                    self.cepage = self.cepage [0:-1]
            self.chang_info()

        self.init()

    def chang_info(self):
        if self.quel_info == 0:
            self.bouton_nom = self.font.render("|" + self.name + "|", True, YELLOW, RED)
        else:
            self.bouton_nom = self.font.render("|" + self.name + "|", True, YELLOW, GRAY)
        self.bouton_nomRect = self.bouton_nom.get_rect()
        self.bouton_nomRect.x = 280
        self.bouton_nomRect.y = 50 + self.decalage_heigh

        if self.quel_info == 1:
            self.bouton_largeur_rang = self.font.render("|" + self.largeur_rang + "|", True, YELLOW, RED)
        else:
            self.bouton_largeur_rang = self.font.render("|" + self.largeur_rang + "|", True, YELLOW, GRAY)
        self.bouton_largeur_rangRect = self.bouton_largeur_rang.get_rect()
        self.bouton_largeur_rangRect.x = 280
        self.bouton_largeur_rangRect.y = 90 + self.decalage_heigh

        if self.quel_info == 2:
            self.bouton_distance_souche = self.font.render("|" + self.distance_souche + "|", True, YELLOW, RED)
        else:
            self.bouton_distance_souche = self.font.render("|" + self.distance_souche + "|", True, YELLOW, GRAY)
        self.bouton_distance_soucheRect = self.bouton_largeur_rang.get_rect()
        self.bouton_distance_soucheRect.x = 280
        self.bouton_distance_soucheRect.y = 130 + self.decalage_heigh

        if self.quel_info == 3:
            self.bouton_cepage = self.font.render("|" + self.cepage + "|", True, YELLOW, RED)
        else:
            self.bouton_cepage = self.font.render("|" + self.cepage + "|", True, YELLOW, GRAY)
        self.bouton_cepageRect = self.bouton_cepage.get_rect()
        self.bouton_cepageRect.x = 280
        self.bouton_cepageRect.y = 170 + self.decalage_heigh

    def save(self):

        if self.name != "" and self.largeur_rang != 0 and self.distance_souche != 0 and self.cepage != "":
            self.parcel.largeur_rang = self.largeur_rang
            self.parcel.distance_souche = self.distance_souche
            self.parcel.cepage = self.cepage

            self.fichier.save_file(self.name, self.parcel) # creer le fichier avec une parcelle vide
            self.fichier.add_name_file_in_list(self.name ) # et ajouter le nom du fichier a la liste qui les gere
            #del(parcel)


            self.screen.blit(self.libelle_saving, self.libelle_savingRect)
            pygame.display.update()
            time.sleep(TIME_MSG)

            self.quel_info = 0
            self.name = ""
            self.largeur_rang = ""
            self.distance_souche = ""
            self.cepage = ""
            self.chang_info()

    def transforme(self):
        print("transforme")
        print(self.window_main.name_parcelle)   
        
        
        self.parcel = self.fichier.load_parcelle(self.window_main.name_parcelle)  
        self.parcel.affiche()

        self.new_parcel.largeur_rang  = self.parcel.largeur_rang
        self.new_parcel.distance_souche = self.parcel.distance_souche
        self.new_parcel.cepage = self.parcel.cepage
        self.new_parcel.tour = self.parcel.tour
        self.new_parcel.rang = self.parcel.rang
        self.new_parcel.vigne = self.parcel.vigne
        self.new_parcel.position_evenement = [(0,0),""]
        self.new_parcelevenement = []
        # j'ai desactive la ligne ci dessou car quand une Parcelle est transforme en NewParcelle et sauvegarde
        # a chaque fois que l'on charge la Parcelle elle est chargé en tant que NewParcelle
        #self.fichier.save_file(self.window_main.name_parcelle, self.new_parcel)

        #self.new_parcel

