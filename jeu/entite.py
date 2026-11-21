"""Classe mère de tout ce qui a une position et une taille sur le terrain,
et le test de collision entre deux rectangles."""


def rectangles_se_chevauchent(zone_a, zone_b):
    """Vérifie si deux rectangles (x, y, largeur, hauteur) se recouvrent.

    :param zone_a: Premier rectangle.
    :type zone_a: tuple[int, int, int, int]
    :param zone_b: Second rectangle au même format.
    :type zone_b: tuple[int, int, int, int]
    :return: True si les rectangles se recouvrent sur les deux axes.
    :rtype: bool
    """
    x_a, y_a, largeur_a, hauteur_a = zone_a
    x_b, y_b, largeur_b, hauteur_b = zone_b
    chevauchement_x = x_a < x_b + largeur_b and x_a + largeur_a > x_b
    chevauchement_y = y_a < y_b + hauteur_b and y_a + hauteur_a > y_b
    return chevauchement_x and chevauchement_y


class Entite:
    """Objet placé sur le terrain : vaisseau, ennemi ou projectile.

    Chaque sous-classe donne sa taille avec LARGEUR et HAUTEUR.
    La position est en lecture seule (@property) : on la change seulement
    avec decaler(), ou dans les méthodes de la classe et de ses sous-classes.
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
        self._x = x
        self._y = y
        self.largeur = self.LARGEUR
        self.hauteur = self.HAUTEUR

    @property
    def x(self):
        """Position horizontale en pixels, en lecture seule."""
        return self._x

    @property
    def y(self):
        """Position verticale en pixels, en lecture seule."""
        return self._y

    def decaler(self, dx, dy=0):
        """Déplace l'entité de quelques pixels.

        :param dx: Décalage horizontal, négatif vers la gauche.
        :type dx: int
        :param dy: Décalage vertical, négatif vers le haut.
        :type dy: int
        """
        self._x += dx
        self._y += dy

    def zone_collision(self):
        """Renvoie le rectangle (x, y, largeur, hauteur) de l'entité.

        Par défaut, (x, y) est le coin en haut à gauche.
        """
        return self.x, self.y, self.largeur, self.hauteur

    def touche(self, autre):
        """Indique si cette entité chevauche une autre entité.

        :param autre: L'autre entité.
        :type autre: Entite
        :rtype: bool
        """
        return rectangles_se_chevauchent(self.zone_collision(), autre.zone_collision())
