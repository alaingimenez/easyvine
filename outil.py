# outil

import config


class Outil:
    def __init__(self):

        self.nom = ""

        # self.list_type = config.LIST_TYPE_OUTILS
        self.type = ""

        #self.list_partie_travaille = config.PARTIE_TRAVAILLE_PAR_LOUTIL
        self.partie_travaille = ""
        
        self.relevage = False   # True si on doit relever en fin de rang 
        self.action_au_cep = False # True si une action doit etre effectue a chaque souche
        self.outil_a_tateur = False

        
        self.largeur_travail= 0  # dans la largeur du rang
        self.longueur_outil = 0  # dans la longeur du rang
        
        
        self.distance_essieu_av_debut_outil = float(0) # distance de l'antenne gps a l'avant de loutil

        self.dist_centre_porteur_centre_outil = float(0) # distance du gps a la partie gauche ou droite de l'outil la plus eloigne du gps
        

        self.penetration_in_intercep = float(0)

    def affiche(self):
        print("nom de l'outil :" + self.nom)
        print("type de l'outil : " + self.type) 
        print("partie travaillé par l'outil : " + self.partie_travaille)
        print("outil a relevage : " + str(self.relevage))
        print("action au cep : " + str(self.action_au_cep))
        print("outil a tateur : " + str(self.outil_a_tateur))
        print("largeur de de travail : " + str(self.largeur_travail)) 
        print("longueur de l'outil : " + str(self.longueur_outil))
        print("distance essieux avant au debut de l'outil : " + str(self.distance_essieu_av_debut_outil))
        print("distance centre porteur au centre de l'outil droite/gauche : " + str(self.dist_centre_porteur_centre_outil))
        print("penetration dans l'intercep : " + str(self.penetration_in_intercep))  

        
