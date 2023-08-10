




BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

import windowalerte

import pygame
pygame.init()

class WindowFichierDelete():
    def __init__(self, screen, fichier):

        self.fichier = fichier # recuperer l'objet fichier qui permet d'avoir acces au sauvegarde et a la liste des fichier

        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf', 50)


        #self.list = window_main.list_name_parcelle
        #self.index_name = window_main.index_list_name_parcelle


        self.list = self.fichier.get_list() # recupere la liste des fichier qu'il y a sur le disk

        self.index_name = 0
        self.name = self.list[self.index_name]


        self.bouton_g = self.font.render(str("<< :"), True, YELLOW, GRAY)  # transformer le texte en graphique
        self.bouton_gRect = self.bouton_g.get_rect()
        self.bouton_gRect.x = 10  # position le texte en width
        self.bouton_gRect.y = 400 # position le texe en heigh en se servant de sa hauteur

        self.bouton_d = self.font.render(str(": >>"), True, YELLOW, GRAY)  # transformer le texte en graphique
        self.bouton_dRect = self.bouton_d.get_rect()
        self.bouton_dRect.x = 600  # position le texte en width
        self.bouton_dRect.y = 400 # position le texe en heigh en se servant de sa hauteur

        self.chang_name()

        self.bouton_delete = self.font.render("|DELETE|", True, YELLOW, GRAY)
        self.bouton_deleteRect = self.bouton_delete.get_rect()
        self.bouton_deleteRect.x = 120
        self.bouton_deleteRect.y = 500


    def init(self):
        self.screen.blit(self.bouton_delete, self.bouton_deleteRect)
        self.screen.blit(self.text_name, self.text_nameRect)
        self.screen.blit(self.bouton_g, self.bouton_gRect)
        self.screen.blit(self.bouton_d, self.bouton_dRect)

    def update(self, event):
        if  event.type == pygame.MOUSEBUTTONDOWN:
            if self.bouton_deleteRect.collidepoint(event.pos):
                self.windowalerte = windowalerte.WindowAlerte(self.screen, "voulez vous detruire le fichier", self.name) # creer la fenetre d'alerte
                if self.windowalerte.update(): # attente de reponse de la fenetre d'alerte
                    self.fichier.delete_file(self.name)
                    self.fichier.del_name_file_in_list(self.name)
                    self.index_name -= 1
                    self.chang_name()
                del self.windowalerte # detruire la fenetre d'alerte

            elif self.bouton_gRect.collidepoint(event.pos):
                self.index_name -= 1

                if self.index_name == -1:
                    self.index_name = len(self.list) - 1
                self.chang_name()


            elif self.bouton_dRect.collidepoint(event.pos):
                self.index_name += 1

                if self.index_name == len(self.list):
                    self.index_name = 0
                self.chang_name()
                #time.sleep(DELAY)


        self.init()


    def chang_name(self): # change le nom du fichier en cour
        self.name = self.list[self.index_name]  # chargement de la liste des parcelle du disk
        self.text_name= self.font.render(str(self.name), True, GREEN,
                                            BLUE)  # transformer le texte en graphique
        self.text_nameRect = self.text_name.get_rect()  # recuperer le rectangle du texte
        self.text_nameRect.x = 120  # position le texte 10 + largeur  bouton gauche  + 5 en width
        self.text_nameRect.y = 400  # position le texe en heigh en se servant de sa hauteur
        self.screen.blit(self.text_name, self.text_nameRect)
        #pygame.display.update()

