"""Déplacement, protection et vies du vaisseau du joueur."""

from .bouclier import Bouclier

class Vaisseau:
    """Représente le vaisseau du joueur et son état pendant la partie.
    """

    LARGEUR = 48

    def __init__(self,x,y):
        """Place le vaisseau avec trois vies.

        :param x: Position du bord gauche en pixels.
        :type x: int
        :param y: Position du bord supérieur en pixels.
        :type y: int
        """
        self.x = x
        self.y = y
        self.largeur = self.LARGEUR
        self.hauteur = 24
        self.vies = 3
        self.bouclier = None

    def deplacer(self, distance, largeur_ecran):
        """Déplace le vaisseau entre les deux bords du terrain.

        :param distance: Déplacement en pixels, négatif vers la gauche.
        :type distance: int
        :param largeur_ecran: Largeur du terrain en pixels.
        :type largeur_ecran: int
        """
        prochain_x = self.x + distance
        limite_droite = largeur_ecran - self.largeur

        if prochain_x < 0:
            prochain_x = 0
        elif prochain_x > limite_droite:
            prochain_x = limite_droite

        self.x = prochain_x

    def zone_collision(self):
        """Renvoie le rectangle du vaisseau.

        :return: Les valeurs (x, y, largeur, hauteur) en pixels.
        :rtype: tuple[int, int, int, int]
        """
        return self.x, self.y, self.largeur, self.hauteur

    def perdre_vie(self):
        """Retire une vie si le vaisseau en a encore."""
        if self.vies > 0:
            self.vies -= 1

    def gagner_vie(self):
        """Ajoute une vie au vaisseau."""
        self.vies += 1

    def activer_bouclier(self):
        """Équipe le vaisseau d'un nouveau bouclier à un impact."""
        self.bouclier = Bouclier()

    def subir_impact(self):
        """Consomme le bouclier actif ou retire une vie au vaisseau."""
        if self.bouclier is not None and self.bouclier.absorber_impact():
            return

        self.perdre_vie()
