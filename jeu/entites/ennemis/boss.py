"""Ennemi résistant qui annonce ses tirs de barrage."""

from .ennemi import Ennemi
from .comportements_tir import TirDeBarrage

class Boss(Ennemi):
    """Ennemi à trois points de vie équipé d'un tir de barrage."""

    def __init__(self, x, y):
        """Crée le boss en conservant le centre de sa case.

        :param x: Bord gauche de la case avant l'ajustement.
        :type x: int
        :param y: Bord supérieur du boss en pixels.
        :type y: int
        """
        super().__init__(x, y, comportement_tir=TirDeBarrage(), pv=3) # On réutilise Ennemi avec super() on file juste 3pv

        self.type_ennemi = "boss"
        centre_x = self.x + self.largeur // 2
        self.largeur = 64
        self.hauteur = 35
        self.x = centre_x - self.largeur // 2

    def colonnes_barrage(self):
        """Renvoie les colonnes que le barrage annonce à cet instant.

        :return: Les abscisses à signaler, ou une liste vide hors
            annonce.
        :rtype: list[int]
        """
        return self.comportement_tir.colonnes_annoncees
