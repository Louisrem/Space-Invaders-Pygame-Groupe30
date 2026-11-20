"""Bonus qui tombent sur le terrain et agissent quand on les ramasse."""

from abc import ABC, abstractmethod


class Bonus(ABC):
    """Regroupe la chute et la collision communes aux bonus.

    Pour ajouter un effet, hérite de Bonus et implémente appliquer().
    Le choix du bonus pour une vague se fait dans BONUS_PAR_VAGUE.
    """
    largeur = 24
    hauteur = 24
    vitesse = 9

    def __init__(self, x, y):
        """Place un bonus sur le terrain.

        :param x: Position du bord gauche en pixels.
        :type x: int
        :param y: Position du bord supérieur en pixels.
        :type y: int
        """
        self.x = x
        self.y = y

    def avancer(self):
        """Fait descendre le bonus d'un tour."""
        self.y += self.vitesse

    def zone_collision(self):
        """Renvoie le rectangle utilisé pour ramasser le bonus.

        :return: Les valeurs (x, y, largeur, hauteur) en pixels.
        :rtype: tuple[int, int, int, int]
        """
        return self.x, self.y, self.largeur, self.hauteur

    def est_sorti_par_le_bas(self, hauteur_ecran):
        """Vérifie si le bonus est entièrement sous l'écran.

        :param hauteur_ecran: Hauteur du terrain en pixels.
        :type hauteur_ecran: int
        :return: True si le bord supérieur du bonus a atteint le bas.
        :rtype: bool
        """
        return self.y >= hauteur_ecran

    @abstractmethod
    def appliquer(self, joueur):
        """Applique l'effet du bonus au vaisseau.

        :param joueur: Vaisseau qui reçoit le bonus.
        :type joueur: Vaisseau
        """
        pass


class Coeur(Bonus):
    """Ajoute une vie au vaisseau qui le ramasse."""

    def appliquer(self, joueur):
        """Ajoute une vie au vaisseau.

        :param joueur: Vaisseau qui ramasse le cœur.
        :type joueur: Vaisseau
        """
        joueur.gagner_vie()


class BonusBouclier(Bonus):
    """Donne un bouclier au vaisseau qui le ramasse."""

    def appliquer(self, joueur):
        """Équipe le vaisseau d'un bouclier actif.

        :param joueur: Vaisseau qui ramasse le bonus.
        :type joueur: Vaisseau
        """
        joueur.activer_bouclier()
