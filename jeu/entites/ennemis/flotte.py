"""Création des formations et déplacement collectif des ennemis."""

from .catalogue import creer_ennemi


class Flotte:
    """Place les ennemis à partir d'une grille et déplace les groupes.
    """

    def __init__(self, grille):
        """Crée les ennemis décrits par les rangées de la vague.

        :param grille: Rangées de la formation, du haut vers le bas.
        :type grille: tuple[str, ...]
        :raises ValueError: Si une lettre est inconnue du catalogue.
        """
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
        """Déplace le groupe si aucun ennemi ne dépasse du terrain.

        :param groupe: Ennemis qui partagent le même mouvement.
        :type groupe: list[Ennemi]
        :param direction: Sens horizontal, -1 vers la gauche ou 1 vers
            la droite.
        :type direction: int
        :param vitesse: Distance parcourue à chaque tour, en pixels.
        :type vitesse: float
        :param largeur_ecran: Largeur du terrain en pixels.
        :type largeur_ecran: int
        :return: La direction à garder et un booléen signalant le bord.
        :rtype: tuple[int, bool]
        """
        distance = direction * vitesse

        for ennemi in groupe: # ici on calcule la position finale
            prochain_x = ennemi.x + distance
            if prochain_x < 0 or prochain_x + ennemi.largeur > largeur_ecran:
                return -direction, True # True c'est si un bord est atteint

        for ennemi in groupe:
            ennemi.x += distance

        return direction, False

    def deplacer(self, largeur_ecran):
        """Avance les deux groupes et fait descendre la flotte au bord.

        Le groupe normal déclenche la descente. Quand seuls les rapides
        restent, leur contact avec le bord déclenche la descente.
        Chaque descente augmente la vitesse des deux groupes.

        :param largeur_ecran: Largeur du terrain en pixels.
        :type largeur_ecran: int
        """
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
            self.vitesse += 0.25
