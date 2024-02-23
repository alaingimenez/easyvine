# porteur



class Porteur:
    def __init__(self):

        self.nom = ""
        self.voie = float(0)
        self.empattement = float(0)
        self.rayon_braquage = float(0)

        self.position_antene_gps = float(0) # par rapport au centre de l'essieux avant 
                                            # du porteur positif vers l'avant positif vers la droite
        
        self.hauteur_antene_gps = float(0)  # hauteur de l'entene par rapport au sol

        
        
        self.type = 0   # 0 = tracteur 3 roues
                        # 1 = tracteur 4 roues 
                        # 2 = enjembeur 3 roues
                        # 3 = enjembeur 4 roues
                        # 4 = tracteur a chenille
        
        self.direction = 0  # 0 = pas de roue directrice type chenille
                            # 1 = roue avant directrice
                            # 2 = roue avant et arriere directrice
                            # 3 = roue arriere directrice
        
        self.vitesse_mini = float(0)
        self.vitesse_max = float(0)

        self.list_outils = [] # liste des outil accepter par le porteur
        self.outil_porte = "" # outil actuellement porté par le porteur

        self.pitch = float(0)   # degre avant arriere
        self.roll = float(0)    # degre droite gauche