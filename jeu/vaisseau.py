"""Déplacement et vies du vaisseau du joueur."""

from .entite import Entite


class Vaisseau(Entite):
    """Représente le vaisseau du joueur."""

    LARGEUR = 48
    HAUTEUR = 24
    VITESSE = 5   # pixels par tour

    def __init__(self, x, y, vies=3):
        """Place le vaisseau avec ses vies de départ.

        :param x: Position du bord gauche en pixels.
        :type x: int
        :param y: Position du bord supérieur en pixels.
        :type y: int
        :param vies: Nombre de vies au départ.
        :type vies: int
        """
        super().__init__(x, y)
        self._vies = vies

    @property
    def vies(self):
        """Nombre de vies restantes, en lecture seule.

        Seule la méthode perdre_vie() peut le modifier.
        """
        return self._vies

    def __repr__(self):
        """Représentation de débogage, par exemple « Vaisseau(x=376, vies=3) »."""
        return f"Vaisseau(x={self.x}, vies={self._vies})"

    def deplacer(self, distance, largeur_ecran):
        """Déplace le vaisseau sans sortir du terrain.

        :param distance: Déplacement en pixels, négatif vers la gauche.
        :type distance: int
        :param largeur_ecran: Largeur du terrain en pixels.
        :type largeur_ecran: int
        """
        limite_droite = largeur_ecran - self.largeur
        self.x = min(max(0, self.x + distance), limite_droite)

    def perdre_vie(self):
        """Retire une vie si le vaisseau en a encore."""
        if self._vies > 0:
            self._vies -= 1
