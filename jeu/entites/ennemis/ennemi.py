"""Ennemi de base auquel on peut associer un tir ou un bouclier."""

from .comportements_tir import SansTir


class Ennemi:
    """Représente un ennemi de la flotte.

    Pour créer une variante dans le catalogue, combine un comportement
    de tir, un bouclier, des points de vie et un groupe de déplacement.
    """

    def __init__(
        self, x, y, comportement_tir=None, rapide=False, bouclier=None, pv=1
    ):
        """Crée un ennemi à sa position de départ.

        :param x: Position du bord gauche en pixels.
        :type x: int
        :param y: Position du bord supérieur en pixels.
        :type y: int
        :param comportement_tir: Règle de tir. Par défaut, l'ennemi ne tire pas.
        :type comportement_tir: ComportementTir | None
        :param rapide: Indique si l'ennemi rejoint le groupe rapide.
        :type rapide: bool
        :param bouclier: Bouclier de l'ennemi, s'il en possède un.
        :type bouclier: Bouclier | None
        :param pv: Nombre de points de vie au départ.
        :type pv: int
        """
        self.type_ennemi = "simple"
        self.x = x
        self.y = y
        self.hauteur = 25
        self.largeur = 40
        self.rapide = rapide
        self.bouclier = bouclier
        self.pv = pv

        if comportement_tir is None:
            comportement_tir = SansTir()

        self.comportement_tir = comportement_tir

    def zone_collision(self):
        """Renvoie le rectangle utilisé pour détecter les impacts.

        :return: Les valeurs (x, y, largeur, hauteur) en pixels.
        :rtype: tuple[int, int, int, int]
        """
        return self.x, self.y, self.largeur, self.hauteur

    def tirer(self):
        """Demande au comportement de tir de décider si un tir part.

        :return: Les projectiles lancés ce tour, ou une liste vide.
        :rtype: list[Projectile]
        """
        return self.comportement_tir.tirer(self)

    def subir_impact(self):
        """Applique un impact au bouclier ou retire un point de vie.

        :return: True si l'ennemi est éliminé, False s'il survit.
        :rtype: bool
        """
        if self.bouclier is not None and self.bouclier.absorber_impact():
            return False

        self.pv -= 1
        return self.pv <= 0