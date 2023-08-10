"""
menu fichier pour selectionner si on va dans :
fichier Creat
ou
Fichier Delete
"""


import fichier
import sys



import windowfichierdelete
import windowfichiercreate

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

#DELAY = 0.2



class WindowFichier:
    def __init__(self, screen):
        self.screen = screen
        self.titre_window = "Fichier"
        self.font = pygame.font.Font('freesansbold.ttf', 50)

        self.actions = [" CREAT  ", " DELETE "]
        self.index_action_actuelle = 0

        self.nom_module = self.font.render(" ** FICHIER **", True, WHITE, BLACK)  # transformer le texte en graphique
        self.nom_moduleRect = self.nom_module.get_rect()
        self.nom_moduleRect.x = 10
        self.nom_moduleRect.y = 10

        self.bouton_g = self.font.render(str("<< :"), True, YELLOW, GRAY)  # transformer le texte en graphique
        self.bouton_gRect = self.bouton_g.get_rect()
        self.bouton_gRect.x = 10  # position le texte en width
        self.bouton_gRect.y = 70  # position le texe en heigh en se servant de sa hauteur

        self.bouton_d = self.font.render(str(": >>"), True, YELLOW, GRAY)  # transformer le texte en graphique
        self.bouton_dRect = self.bouton_d.get_rect()
        self.bouton_dRect.x = 350  # position le texte en width
        self.bouton_dRect.y = 70  # position le texe en heigh en se servant de sa hauteur

        self.chang_action()

        self.init()

        """
        self.name_action = self.actions[self.index_action_actuelle]  # chargement de la liste /PARCELLE/ /RANG/
        self.text_action = self.font.render(str(self.name_action), True, GREEN,
                                            BLUE)  # transformer le texte en graphique
        self.text_actionRect = self.text_action.get_rect()  # recuperer le rectangle du texte
        self.text_actionRect.x = 65  # position le texte 10 + largeur  bouton gauche  + 5 en width
        self.text_actionRect.y = 10  # position le texe en heigh en se servant de sa hauteur
        """
    def init(self):
        #pygame.display.set_caption(self.titre_window)



        self.screen.blit(self.bouton_g, self.bouton_gRect)
        self.screen.blit(self.bouton_d,self.bouton_dRect)
        self.screen.blit(self.text_action,self.text_actionRect)
        self.screen.blit(self.nom_module, self.nom_moduleRect)

    """
    def update(self, event):
        if  event.type == pygame.MOUSEBUTTONDOWN:
            if self.bouton_gRect.collidepoint(event.pos):
                self.index_action_actuelle -= 1

                if self.index_action_actuelle == -1:
                    self.index_action_actuelle = len(self.actions) - 1
                self.chang_action()
                #time.sleep(DELAY)

            elif self.bouton_dRect.collidepoint(event.pos):
                self.index_action_actuelle += 1

                if self.index_action_actuelle == len(self.actions):
                    self.index_action_actuelle = 0
                self.chang_action()
                #time.sleep(DELAY)

        self.init()
        return self.index_action_actuelle
    """

    def chang_action(self):
        self.name_action = self.actions[self.index_action_actuelle]  # chargement de la liste /PARCELLE/ /RANG/
        self.text_action = self.font.render(str(self.name_action), True, GREEN,
                                            BLUE)  # transformer le texte en graphique
        self.text_actionRect = self.text_action.get_rect()  # recuperer le rectangle du texte
        self.text_actionRect.x = 120 # position le texte 10 + largeur  bouton gauche  + 5 en width
        self.text_actionRect.y = 70 # position le texe en heigh en se servant de sa hauteur
        self.screen.blit(self.text_action, self.text_actionRect)
        #pygame.display.update()




def gestion(window_m):
    window_main = window_m
    screen = window_main.screen

    window_fichier = WindowFichier(screen)
    fichier_obj = window_main.fichier   # fichier.Fichier()


    window_fichier_create = windowfichiercreate.WindowFichierCreate(screen, fichier_obj,window_main)
    window_fichier_delete = windowfichierdelete.WindowFichierDelete(screen, fichier_obj)



    while True:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window_main.index_action = -99 # permet de fermer le programe
                return 0
                #pygame.quit()
                #sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if window_main.bouton_action_gRect.collidepoint(event.pos): # permet de sortir de la windowfichier
                    module = window_main.dec_action_actuelle()
                    print(" click bouton gazuche fichier module", module)
                    pygame.Surface.fill(screen, BLACK)
                    window_main.update()  # # affiche a l'ecran les texte
                    del(window_main)
                    del(window_fichier)
                    del(window_fichier_create)
                    del(window_fichier_delete)
                    del(fichier_obj )
                    return module
                elif window_main.bouton_action_dRect.collidepoint(event.pos): # permet de sortir de la windowfichier
                    module = window_main.inc_action_actuelle()
                    print(" click bouton gazuche fichier module", module)
                    pygame.Surface.fill(screen, BLACK)
                    window_main.update()  # # affiche a l'ecran les texte
                    del (window_main)
                    del (window_fichier)
                    del (window_fichier_create)
                    del (window_fichier_delete)
                    del (fichier_obj)
                    return module
                elif window_main.bouton_parcelle_gRect.collidepoint(event.pos):
                    window_main.dec_index_parcelle()
                elif window_main.bouton_parcelle_dRect.collidepoint(event.pos):
                    window_main.inc_index_parcelle()

                elif window_fichier.bouton_gRect.collidepoint(event.pos): # premet de changer l'action CREAT/DELETE
                    window_fichier.index_action_actuelle -= 1
                    if window_fichier.index_action_actuelle == -1:
                        window_fichier.index_action_actuelle = len(window_fichier.actions) - 1
                elif window_fichier.bouton_dRect.collidepoint(event.pos): # premet de changer l'action CREAT/DELETE
                    window_fichier.index_action_actuelle += 1
                    if window_fichier.index_action_actuelle == len(window_fichier.actions):
                        window_fichier.index_action_actuelle = 0
                window_fichier.chang_action() # actualise de texte de l'action en cour a l'ecran

            pygame.Surface.fill(screen, BLACK)
            if window_fichier.index_action_actuelle == 0:
                window_fichier_create.update(event)
            elif window_fichier.index_action_actuelle == 1:
                window_fichier_delete.update(event)

        window_main.update()    # # affiche a l'ecran les texte
        window_fichier.init() # affiche a l'ecran les texte de la fenetre window_fichier
        pygame.display.update()

