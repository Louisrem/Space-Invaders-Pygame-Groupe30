from abc import ABC, abstractmethod


class Bonus(ABC):
    largeur = 24
    hauteur = 24
    vitesse = 9

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def avancer(self):
        self.y += self.vitesse

    def zone_collision(self):
        return self.x, self.y, self.largeur, self.hauteur

    def est_sorti_par_le_bas(self, hauteur_ecran):
        return self.y >= hauteur_ecran

    @abstractmethod
    def appliquer(self, joueur):
        pass


class Coeur(Bonus):
    def appliquer(self, joueur):
        joueur.gagner_vie()


class BonusBouclier(Bonus):
    def appliquer(self, joueur):
        joueur.activer_bouclier()
