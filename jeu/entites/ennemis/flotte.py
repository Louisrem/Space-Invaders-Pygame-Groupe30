from .catalogue import creer_ennemi


class Flotte:
    def __init__(self, grille):
        self.ennemis = []
        self.direction = 1
        self.direction_rapides = 1
        self.vitesse = 2

        for ligne, rangee in enumerate(grille):
            for colonne, case in enumerate(rangee):
                if case == ".":
                    continue
                x = 230 + colonne * 75
                y = 60 + ligne * 45

                self.ennemis.append(creer_ennemi(case, x, y))

    def _deplacer_groupe(self, groupe, direction, vitesse, largeur_ecran):
        distance = direction * vitesse

        for ennemi in groupe: # ici on calcule la position finale
            prochain_x = ennemi.x + distance
            if prochain_x < 0 or prochain_x + ennemi.largeur > largeur_ecran:
                return -direction, True # True c'est si un bord est atteint

        for ennemi in groupe:
            ennemi.x += distance

        return direction, False

    def deplacer(self, largeur_ecran):
        lents = [ennemi for ennemi in self.ennemis if not ennemi.rapide]
        rapides = [ennemi for ennemi in self.ennemis if ennemi.rapide]

        self.direction, bord_lents = self._deplacer_groupe(
            lents, self.direction, self.vitesse, largeur_ecran
        )
        self.direction_rapides, bord_rapides = self._deplacer_groupe(
            rapides, self.direction_rapides, self.vitesse + 1, largeur_ecran
        )

        if bord_lents or (not lents and bord_rapides):
            for ennemi in self.ennemis:
                ennemi.y += 25
