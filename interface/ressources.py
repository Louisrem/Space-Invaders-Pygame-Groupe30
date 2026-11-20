from pathlib import Path

import pygame

from jeu.entites.ennemis.catalogue import CATALOGUE_ENNEMIS


DOSSIER_IMAGES = Path(__file__).resolve().parent.parent / "assets" / "images"

def charger_fond(taille):
    image = pygame.image.load(DOSSIER_IMAGES / "fonds" / "orbite.png").convert()
    return pygame.transform.smoothscale(image, taille)


def charger_sprite_vaisseau(taille):
    sprite = pygame.image.load(DOSSIER_IMAGES / "vaisseau.png").convert_alpha()
    return pygame.transform.scale(sprite, taille)

def _charger_sprites(dossier, noms):
    chemin = DOSSIER_IMAGES / dossier
    return {
        nom: pygame.image.load(chemin / f"{nom}.png").convert_alpha()
        for nom in noms
    }

def charger_sprites_ennemis():
    noms = [nom for nom, _ in CATALOGUE_ENNEMIS.values()]
    return _charger_sprites("ennemis", noms)

def charger_sprites_projectiles():
    noms = ("tir_joueur", "tir_ennemi", "tir_boss", "mine", "mine_armee")
    return _charger_sprites("projectiles", noms)
