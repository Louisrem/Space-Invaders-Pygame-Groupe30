"""Classe mère de tout ce qui a une position et une taille sur le terrain."""


class Entite:
    """Objet placé sur le terrain : vaisseau, ennemi ou projectile.

    Chaque sous-classe donne sa taille avec LARGEUR et HAUTEUR.
    """

    LARGEUR = 0
    HAUTEUR = 0

    def __init__(self, x, y):
        """Place l'entité sur le terrain.

        :param x: Position horizontale en pixels.
        :type x: int
        :param y: Position verticale en pixels.
        :type y: int
        """
        self.x = x
        self.y = y
        self.largeur = self.LARGEUR
        self.hauteur = self.HAUTEUR

    def zone_collision(self):
        """Renvoie le rectangle (x, y, largeur, hauteur) de l'entité.

        Par défaut, (x, y) est le coin en haut à gauche.
        """
        return self.x, self.y, self.largeur, self.hauteur
