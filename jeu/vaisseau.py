class Vaisseau:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.largeur = 40
        self.hauteur = 20

    def deplacer(self, distance, largeur_ecran):
        prochain_x = self.x + distance
        limite_droite = largeur_ecran - self.largeur

        if prochain_x < 0:
            prochain_x = 0
        elif prochain_x > limite_droite:
            prochain_x = limite_droite

        self.x = prochain_x