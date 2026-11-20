from .bouclier import Bouclier

class Vaisseau:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.largeur = 48
        self.hauteur = 24
        self.vies = 3
        self.bouclier = None

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

    def gagner_vie(self):
        self.vies += 1

    def activer_bouclier(self):
        self.bouclier = Bouclier()

    def subir_impact(self):
        if self.bouclier is not None and self.bouclier.absorber_impact():
            return

        self.perdre_vie()
