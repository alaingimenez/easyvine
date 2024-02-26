# outil

import config


class Outil:
    def __init__(self):

        self.nom = ""

        self.list_type = config.LIST_TYPE_OUTILS

        self.list_partie_travaille = config.PARTIE_TRAVAILLE_PAR_LOUTIL
        
        self.relevage = False   # True si on doit relever en fin de rang 
        self.action_au_cep = False # True si une action doit etre effectue a chaque souche
        self.outil_a_tateur = False

        
        self.largeur_travail= 0  # dans la largeur du rang
        self.longeur_outil = 0  # dans la longeur du rang
        
        
        self.distance_gps_debut_outil = float(0) # distance de l'antenne gps a l'avant de loutil
        self.distance_gps_exterieur_outil = float(0) # distance du gps a la partie gauche ou droite de l'outil la plus eloigne du gps

        self.penetration_in_intercep = float(0)

        
