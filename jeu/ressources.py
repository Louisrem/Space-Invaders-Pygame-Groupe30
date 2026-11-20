from pathlib import Path

import pygame


DOSSIER_IMAGES = Path(__file__).resolve().parent.parent / "assets" / "images"


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
    return _charger_sprites("ennemis", ("simple", "tireur", "rapide", "protege", "boss"))


def charger_sprites_projectiles():
    return _charger_sprites("projectiles", ("tir_joueur", "tir_ennemi", "mine", "mine_armee"))
