"""Tout l'affichage Pygame : chargement des images et dessin de la partie."""

from pathlib import Path

import pygame

from jeu.constantes import EtatPartie
from jeu.ennemis import Boss, Ennemi, Tireur
from jeu.projectiles import Mine, Projectile
from jeu.vaisseau import Vaisseau

DOSSIER_ASSETS = Path(__file__).resolve().parent.parent / "assets"
DOSSIER_IMAGES = DOSSIER_ASSETS / "images"

# Fichiers PNG à charger, rangés par sous-dossier de assets/images/.
FICHIERS_IMAGES = {
    "ennemis": ("simple", "tireur", "boss"),
    "projectiles": ("tir_joueur", "tir_ennemi", "mine", "mine_armee"),
}

# Classe -> nom de l'image (ou fonction qui le choisit selon l'état de l'objet).
# C'est l'interface qui choisit les images : jeu/ ne connaît aucun fichier.
# Une sous-classe sans ligne ici prend l'image de sa classe mère.
IMAGES = {
    Ennemi: "simple",
    Tireur: "tireur",
    Boss: "boss",
    Projectile: lambda tir: "tir_joueur" if tir.direction < 0 else "tir_ennemi",
    Mine: lambda mine: "mine_armee" if mine.armee else "mine",
}
BLANC = (255, 255, 255)


def _charger(chemin):
    """Charge une image PNG transparente."""
    return pygame.image.load(chemin).convert_alpha()


def charger_images(taille_ecran):
    """Charge toutes les images du jeu.

    :param taille_ecran: Largeur et hauteur de la fenêtre.
    :type taille_ecran: tuple[int, int]
    :return: Les images indexées par nom (fond, vaisseau, ennemis, tirs).
    :rtype: dict[str, pygame.Surface]
    """
    fond = pygame.image.load(DOSSIER_IMAGES / "fonds" / "orbite.png").convert()
    vaisseau = _charger(DOSSIER_IMAGES / "vaisseau.png")

    images = {
        "fond": pygame.transform.smoothscale(fond, taille_ecran),
        "vaisseau": pygame.transform.scale(vaisseau, (Vaisseau.LARGEUR, Vaisseau.HAUTEUR)),
    }
    for dossier, noms in FICHIERS_IMAGES.items():
        for nom in noms:
            images[nom] = _charger(DOSSIER_IMAGES / dossier / f"{nom}.png")
    return images


def nom_image(objet):
    """Trouve le nom de l'image d'un ennemi ou d'un projectile.

    On remonte les classes de l'objet (type(objet).__mro__) : la classe
    elle-même d'abord, puis sa classe mère, etc. Une nouvelle sous-classe
    sans image à elle prend donc celle de sa classe mère.

    :raises KeyError: Si aucune classe de l'objet n'a d'image.
    """
    for classe in type(objet).__mro__:
        if classe in IMAGES:
            image = IMAGES[classe]
            return image(objet) if callable(image) else image
    raise KeyError(f"Pas d'image pour {type(objet).__name__}")


def dessiner_texte(ecran, police, texte, centre):
    """Dessine un texte blanc centré sur un point."""
    image = police.render(texte, True, BLANC)
    ecran.blit(image, image.get_rect(center=centre))


def dessiner_partie(ecran, police, partie, images):
    """Dessine le terrain, les entités et le tableau de bord.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param partie: Partie dont on affiche l'état.
    :type partie: Partie
    :param images: Images chargées par charger_images().
    :type images: dict[str, pygame.Surface]
    """
    ecran.blit(images["fond"], (0, 0))
    joueur = partie.joueur
    ecran.blit(images["vaisseau"], (joueur.x, joueur.y))

    for ennemi in partie.flotte:
        ecran.blit(images[nom_image(ennemi)], (ennemi.x, ennemi.y))

    for projectile in partie.projectiles_joueur + partie.projectiles_ennemis:
        x, y, _, _ = projectile.zone_collision()
        ecran.blit(images[nom_image(projectile)], (x, y))

    largeur = ecran.get_width()
    ecran.blit(police.render(f"Score : {partie.score}", True, BLANC), (15, 15))
    ecran.blit(police.render(f"Vies : {joueur.vies}", True, BLANC), (15, 40))
    dessiner_texte(ecran, police, f"Vague {partie.niveau}", (largeur // 2, 25))

    if partie.etat == EtatPartie.MENU:
        dessiner_texte(ecran, police, "SPACE INVADERS", (largeur // 2, 300))
        dessiner_texte(ecran, police, "Entrée pour jouer", (largeur // 2, 340))
    elif partie.etat in (EtatPartie.VICTOIRE, EtatPartie.DEFAITE):
        titre = "VICTOIRE !" if partie.etat == EtatPartie.VICTOIRE else "PARTIE TERMINÉE"
        dessiner_texte(ecran, police, titre, (largeur // 2, 300))
        dessiner_texte(ecran, police, "Entrée pour rejouer", (largeur // 2, 340))
