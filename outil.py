# outil


class Outil:
    def __init__(self):

        self.nom = ""

        self.type = 0   # 0 = pas d'outil
                        # 1 = lame
                        # 2 = tondeuse axe vertical
                        # 3 = tondeuse axe horizontal
                        # 4 = arrosage
                        # 5 = pulve traitement
                        # 6 = pulve desherbage
                        # 7 = distributeur engrais
        
        self.travail_x = 0  # dans la largeur du rang
        self.travail_y = 0  # dans la longeur du rang
        
        
        self.distance_essieu_avant_debut_travail_y = float(0)
        self.distance_centre_porteur_debut_travail_x = float(0)

        self.penetration_in_intercep = float(0)

        self.relevage = False   # True si on doit relever en fin de rang 
        self.attention_cep = False # True si une action doit etre effectue a chaque souche
