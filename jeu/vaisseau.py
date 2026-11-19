class Vaisseau:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.largeur = 40
        self.hauteur = 20
        self.vies = 3

    def deplacer(self, distance, largeur_ecran):
        prochain_x = self.x + distance
        limite_droite = largeur_ecran - self.largeur

        if prochain_x < 0:
            prochain_x = 0
        elif prochain_x > limite_droite:
            prochain_x = limite_droite

        self.x = prochain_x

    def zone_collision(self):
        return self.x, self.y, self.largeur, self.hauteur

    def perdre_vie(self):
        if self.vies > 0:
            self.vies -= 1