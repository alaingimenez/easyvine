"""
cree une fenetre d'alerte
retourne True pour OUI False pour NON

"""

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

import sys
import pygame
pygame.init()

class WindowAlerte():
    def __init__(self,screen, action, message): # action sera: DELETE ou SAV  message sera: le nom du fichier
        self.screen = screen
        self.action = action
        self.message = message
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.font_un = pygame.font.Font('freesansbold.ttf', 50)

        self.titre = self.font.render(" ALERTE ", True, RED, BLACK)  # transformer le texte en graphique
        self.titreRect = self.titre.get_rect()
        self.titreRect.x = 350  # position le texte en width
        self.titreRect.y = 250  # position le texe en heigh en se servant de sa hauteur

        self.text_action = self.font.render(self.action, True, WHITE, BLACK)  # transformer le texte en graphique
        self.text_actionRect = self.text_action.get_rect()
        self.text_actionRect.x = 200  # position le texte en width
        self.text_actionRect.y = 300  # position le texe en heigh en se servant de sa hauteur

        self.text_message = self.font.render(self.message, True, GREEN, BLACK)  # transformer le texte en graphique
        self.text_messageRect = self.text_message.get_rect()
        self.text_messageRect.x = 200  # position le texte en width
        self.text_messageRect.y = 350  # position le texe en heigh en se servant de sa hauteur


        self.buton_oui = self.font_un.render("| OUI |", True, YELLOW, GRAY)  # transformer le texte en graphique
        self.buton_ouiRect = self.buton_oui.get_rect()
        self.buton_ouiRect.x = 200  # position le texte en width
        self.buton_ouiRect.y = 450  # position le texe en heigh en se servant de sa hauteur

        self.buton_non = self.font_un.render("| NON |", True, YELLOW, GRAY)  # transformer le texte en graphique
        self.buton_nonRect = self.buton_non.get_rect()
        self.buton_nonRect.x = 500  # position le texte en width
        self.buton_nonRect.y = 450  # position le texe en heigh en se servant de sa hauteur
        self.choix = False

        self.init()


    def init(self):
        deb_x = 170
        deb_y = 220
        fin_x = 700
        fin_y = 530
        pygame.draw.rect(self.screen, BLACK,(deb_x, deb_y, fin_x, fin_y))
        pygame.draw.lines(self.screen, RED, True, [(deb_x, deb_y), (fin_x, deb_y), (fin_x, fin_y), (deb_x, fin_y)], 10)
        self.screen.blit(self.titre, self.titreRect)
        self.screen.blit(self.text_action, self.text_actionRect)
        self.screen.blit(self.text_message, self.text_messageRect)
        self.screen.blit(self.buton_oui, self.buton_ouiRect)
        self.screen.blit(self.buton_non, self.buton_nonRect)
        pygame.display.update()



    def update(self):
        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buton_ouiRect.collidepoint(event.pos):
                        self.choix = True
                        is_running = False
                    elif self.buton_nonRect.collidepoint(event.pos):
                        self.choix = False
                        is_running = False

        return self.choix