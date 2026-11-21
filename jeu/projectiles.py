"""Les armes du jeu (tir normal et mine) et le test de collision.

Pour ajouter une arme, hérite de Projectile et redéfinis avancer() ou
ennemis_touches(). La partie traite toutes les armes de la même façon
(polymorphisme) : il suffit ensuite d'associer une touche dans main.py.
"""

from .constantes import HAUTEUR_TERRAIN, EvenementPartie


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


class Projectile:
    """Tir vertical qui touche le premier ennemi rencontré.

    Utilisé par le joueur (vers le haut) et par les ennemis (vers le bas).
    """

    LARGEUR = 6
    HAUTEUR = 12
    VITESSE = 8
    EVENEMENT_TIR = EvenementPartie.TIR_JOUEUR
    EVENEMENT_IMPACT = None

    def __init__(self, x, y, direction=-1):
        """Place un tir à l'endroit où il apparaît.

        :param x: Centre horizontal du tir en pixels.
        :type x: int
        :param y: Bord inférieur du tir en pixels.
        :type y: int
        :param direction: -1 vers le haut ou 1 vers le bas.
        :type direction: int
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.largeur = self.LARGEUR
        self.hauteur = self.HAUTEUR

    def __repr__(self):
        """Représentation de débogage, par exemple « Mine(x=400, y=316) »."""
        return f"{type(self).__name__}(x={self.x}, y={self.y})"

    def avancer(self):
        """Déplace le tir d'un tour dans sa direction."""
        self.y += self.VITESSE * self.direction

    def zone_collision(self):
        """Renvoie le rectangle (x, y, largeur, hauteur) du tir."""
        return self.x - self.largeur // 2, self.y - self.hauteur, self.largeur, self.hauteur

    def est_sorti(self, hauteur_ecran):
        """Indique si le tir a quitté le terrain par le haut ou par le bas."""
        return self.y <= 0 or self.y - self.hauteur >= hauteur_ecran

    def ennemis_touches(self, ennemis):
        """Renvoie les ennemis touchés à ce tour.

        :param ennemis: Ennemis encore en jeu.
        :type ennemis: Iterable[Ennemi]
        :return: Le premier ennemi touché, ou une liste vide.
        :rtype: list[Ennemi]
        """
        for ennemi in ennemis:
            if rectangles_se_chevauchent(self.zone_collision(), ennemi.zone_collision()):
                return [ennemi]
        return []


class Mine(Projectile):
    """Monte jusqu'au milieu du terrain, puis explose près d'un ennemi.

    Elle redéfinit avancer() (elle s'arrête) et ennemis_touches() (elle
    touche tous les ennemis dans son rayon d'explosion).
    """

    LARGEUR = 16
    HAUTEUR = 16
    EVENEMENT_TIR = EvenementPartie.MINE_LANCEE
    EVENEMENT_IMPACT = EvenementPartie.EXPLOSION_MINE
    RAYON_DETECTION = 22
    RAYON_EXPLOSION = 65

    def __init__(self, x, y):
        """Prépare une mine qui s'arrête au milieu du terrain."""
        super().__init__(x, y)
        self._y_arret = HAUTEUR_TERRAIN // 2 + self.hauteur // 2

    @property
    def armee(self):
        """Indique si la mine a atteint sa position d'arrêt."""
        return self.y <= self._y_arret

    def avancer(self):
        """Fait monter la mine jusqu'à sa hauteur d'arrêt."""
        if not self.armee:
            super().avancer()
            self.y = max(self.y, self._y_arret)

    def ennemis_touches(self, ennemis):
        """Explose si un ennemi est assez proche de la mine armée.

        :return: Tous les ennemis dans le rayon d'explosion, ou une liste
            vide si la mine n'explose pas encore.
        :rtype: list[Ennemi]
        """
        ennemis = list(ennemis)
        if not self.armee:
            return []
        if not any(self._dans_rayon(e, self.RAYON_DETECTION) for e in ennemis):
            return []
        return [e for e in ennemis if self._dans_rayon(e, self.RAYON_EXPLOSION)]

    def _dans_rayon(self, ennemi, rayon):
        """Vérifie si le rectangle d'un ennemi touche un cercle centré sur la mine."""
        gauche, haut, largeur, hauteur = ennemi.zone_collision()
        x, y = self.x, self.y - self.hauteur // 2
        proche_x = max(gauche, min(x, gauche + largeur))
        proche_y = max(haut, min(y, haut + hauteur))
        return (x - proche_x) ** 2 + (y - proche_y) ** 2 <= rayon ** 2
