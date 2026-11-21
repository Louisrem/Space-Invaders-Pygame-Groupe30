"""Déplacement et collisions des tirs, des barrages et des mines."""

class Projectile:
    """Représente un tir vertical utilisé par le joueur ou les ennemis.
    """

    LARGEUR = 6

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
        self.vitesse = 8
        self.largeur = self.LARGEUR
        self.hauteur = 12
        self.direction = direction

    def avancer(self):
        """Déplace le tir d'un tour dans sa direction."""
        self.y = self.y + self.vitesse * self.direction

    def zone_collision(self):
        """Convertit la position du tir en rectangle de collision.

        :return: Le bord gauche, le haut, la largeur et la hauteur en
            pixels.
        :rtype: tuple[int, int, int, int]
        """
        gauche = self.x - self.largeur // 2
        haut = self.y - self.hauteur
        return gauche, haut, self.largeur, self.hauteur

    def est_sorti_par_le_haut(self):
        """Vérifie si le tir est entièrement sorti par le haut.

        :return: True si le tir est entièrement sorti par le haut.
        :rtype: bool
        """
        return self.y <= 0

    def est_sorti_par_le_bas(self, hauteur_ecran):
        """Indique si le tir est entièrement sorti par le bas.

        :param hauteur_ecran: Hauteur du terrain en pixels.
        :type hauteur_ecran: int
        :return: True si le bord supérieur du tir a atteint le bas.
        :rtype: bool
        """
        haut = self.y - self.hauteur
        return haut >= hauteur_ecran

class ProjectileBarrage(Projectile):
    """Représente un tir descendant du barrage du boss."""

    def __init__(self, x):
        """Prépare un tir de barrage qui arrive du haut du terrain.

        :param x: Colonne annoncée par le barrage, en pixels.
        :type x: int
        """
        super().__init__(x, 0, direction=1)


class Mine(Projectile):
    """Monte jusqu'à sa hauteur d'arrêt et attend un ennemi à proximité.

    Le rayon de détection déclenche la mine. Le rayon d'explosion, plus
    large, détermine les ennemis qui subissent un impact dans Partie.
    """
    rayon_detection = 22
    rayon_explosion = 65

    def __init__(self, x, y, hauteur_arret):
        """Prépare une mine qui monte jusqu'à la hauteur choisie.

        :param x: Centre horizontal de départ en pixels.
        :type x: int
        :param y: Bord inférieur de départ en pixels.
        :type y: int
        :param hauteur_arret: Position verticale du centre une fois la
            mine armée.
        :type hauteur_arret: int
        """
        super().__init__(x, y)
        self.largeur = 16
        self.hauteur = 16
        self.y_arret = hauteur_arret + self.hauteur // 2

    @property
    def centre(self):
        """Renvoie le centre géométrique de la mine.

        :return: Les coordonnées (x, y) du centre en pixels.
        :rtype: tuple[int, int]
        """
        return self.x, self.y - self.hauteur // 2

    @property
    def armee(self):
        """Indique si la mine a atteint sa position d'arrêt."""
        return self.y <= self.y_arret

    def avancer(self):
        """Fait monter la mine jusqu'à sa hauteur d'arrêt."""
        if not self.armee:
            super().avancer()
            self.y = max(self.y, self.y_arret)

    def dans_rayon(self, zone, rayon):
        """Vérifie si un rectangle touche un cercle centré sur la mine.

        :param zone: Rectangle (x, y, largeur, hauteur) à vérifier.
        :type zone: tuple[int, int, int, int]
        :param rayon: Rayon de détection ou d'explosion, en pixels.
        :type rayon: int
        :return: True si le point du rectangle le plus proche est dans
            le rayon.
        :rtype: bool
        """
        gauche, haut, largeur, hauteur = zone
        x, y = self.centre
        proche_x = max(gauche, min(x, gauche + largeur))
        proche_y = max(haut, min(y, haut + hauteur))
        return (x - proche_x) ** 2 + (y - proche_y) ** 2 <= rayon ** 2
