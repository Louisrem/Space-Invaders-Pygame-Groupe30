from jeu.ennemis import Ennemi
from jeu.ennemis.comportements_tir import TirSimple

class Flotte:
    def __init__(self, grille):
        self.ennemis = []
        self.direction = 1
        self.vitesse = 2

        for ligne, rangee in enumerate(grille):
            for colonne, case in enumerate(rangee):
                if case == ".":
                    continue
                x = 230 + colonne * 75
                y = 60 + ligne * 45

                if case == "N":
                    ennemi = Ennemi(x, y)
                elif case == "T":
                    ennemi = Ennemi(x, y, TirSimple())
                else:
                    raise ValueError(f"Case de vague inconnue : {case}")

                self.ennemis.append(ennemi)

    def deplacer(self, largeur_ecran):
        distance = self.direction * self.vitesse

        for ennemi in self.ennemis:
            prochain_x = ennemi.x + distance
            if prochain_x < 0 or prochain_x + ennemi.largeur > largeur_ecran:
                self.direction = -self.direction

                for membre in self.ennemis:
                    membre.y += 25

                return

        for ennemi in self.ennemis:
            ennemi.x += distance