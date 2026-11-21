"""Catalogue des lettres de vagues et flotte d'ennemis."""

from .ennemis import Boss, Ennemi, Tireur

# "lettre": classe de l'ennemi.
# Pour ajouter un ennemi : crée sa classe dans ennemis.py, ajoute une lettre
# ici, puis utilise la lettre dans vagues.py. Son image se déclare dans
# interface/affichage.py.
CATALOGUE_ENNEMIS = {
    "N": Ennemi,
    "T": Tireur,
    "B": Boss,
}


def creer_ennemi(case, x, y):
    """Crée l'ennemi correspondant à une lettre de la grille.

    :raises ValueError: Si la lettre est absente du catalogue.
    """
    try:
        classe = CATALOGUE_ENNEMIS[case]
    except KeyError:
        raise ValueError(f"Case de vague inconnue : {case}") from None
    return classe(x, y)


class Flotte:
    """Place les ennemis à partir d'une grille et les déplace en bloc.

    La flotte est itérable : on peut écrire « for ennemi in flotte » et
    « len(flotte) ».
    """

    VITESSE = 2
    DESCENTE = 25
    # Placement de la grille au début d'une vague (en pixels)
    X_DEPART = 230      # bord gauche de la première colonne
    Y_DEPART = 60       # haut de la première rangée
    ECART_COLONNES = 75
    ECART_RANGEES = 45

    def __init__(self, grille):
        """Crée les ennemis décrits par les rangées de la vague.

        :param grille: Rangées de la formation, du haut vers le bas.
        :type grille: tuple[str, ...]
        """
        self._ennemis = []
        self._direction = 1

        for ligne, rangee in enumerate(grille):
            for colonne, case in enumerate(rangee):
                if case != ".":
                    x = self.X_DEPART + colonne * self.ECART_COLONNES
                    y = self.Y_DEPART + ligne * self.ECART_RANGEES
                    self._ennemis.append(creer_ennemi(case, x, y))

    def __iter__(self):
        """Parcourt les ennemis encore en jeu (générateur)."""
        yield from self._ennemis

    def __len__(self):
        """Renvoie le nombre d'ennemis encore en jeu."""
        return len(self._ennemis)

    def retirer(self, ennemi):
        """Retire un ennemi éliminé de la flotte."""
        self._ennemis.remove(ennemi)

    def deplacer(self, largeur_ecran):
        """Avance la flotte, ou la fait descendre et repartir au bord.

        :param largeur_ecran: Largeur du terrain en pixels.
        :type largeur_ecran: int
        """
        distance = self._direction * self.VITESSE
        touche_bord = any(
            e.x + distance < 0 or e.x + e.largeur + distance > largeur_ecran
            for e in self._ennemis
        )

        if touche_bord:
            self._direction = -self._direction
            for ennemi in self._ennemis:
                ennemi.y += self.DESCENTE
        else:
            for ennemi in self._ennemis:
                ennemi.x += distance
