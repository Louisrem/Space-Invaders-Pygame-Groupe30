"""Charge les images Pygame après l'ouverture de la fenêtre."""

from pathlib import Path

import pygame

from jeu.entites.ennemis.catalogue import CATALOGUE_ENNEMIS


DOSSIER_IMAGES = Path(__file__).resolve().parent.parent / "assets" / "images"

def charger_fond(taille):
    """Charge le fond orbital et l'adapte aux dimensions du terrain.

    :param taille: Largeur et hauteur de la fenêtre en pixels.
    :type taille: tuple[int, int]
    :return: Le fond prêt à être affiché.
    :rtype: pygame.Surface
    """
    image = pygame.image.load(DOSSIER_IMAGES / "fonds" / "orbite.png").convert()
    return pygame.transform.smoothscale(image, taille)


def charger_sprite_vaisseau(taille):
    """Charge le sprite du vaisseau et l'adapte à sa hitbox.

    :param taille: Largeur et hauteur de la hitbox en pixels.
    :type taille: tuple[int, int]
    :return: Le sprite redimensionné avec sa transparence.
    :rtype: pygame.Surface
    """
    sprite = pygame.image.load(DOSSIER_IMAGES / "vaisseau.png").convert_alpha()
    return pygame.transform.scale(sprite, taille)

def _charger_sprites(dossier, noms):
    """Charge les PNG transparents d'un dossier sous assets/images.

    :param dossier: Sous-dossier des images.
    :type dossier: str
    :param noms: Noms des fichiers sans l'extension PNG.
    :type noms: Iterable[str]
    :return: Les surfaces chargées, indexées par nom.
    :rtype: dict[str, pygame.Surface]
    """
    chemin = DOSSIER_IMAGES / dossier
    return {
        nom: pygame.image.load(chemin / f"{nom}.png").convert_alpha()
        for nom in noms
    }

def charger_sprites_ennemis():
    """Charge les sprites référencés dans le catalogue des ennemis.

    :return: Les surfaces indexées par type d'ennemi.
    :rtype: dict[str, pygame.Surface]
    """
    noms = [nom for nom, _ in CATALOGUE_ENNEMIS.values()]
    return _charger_sprites("ennemis", noms)

def charger_sprites_projectiles():
    """Charge les PNG des tirs et les deux états visuels de la mine.

    :return: Les surfaces indexées par nom de sprite.
    :rtype: dict[str, pygame.Surface]
    """
    noms = ("tir_joueur", "tir_ennemi", "tir_boss", "mine", "mine_armee")
    return _charger_sprites("projectiles", noms)
