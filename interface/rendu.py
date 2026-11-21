"""Affichage du terrain, des objets et du tableau de bord."""

from functools import lru_cache
from math import pi

import pygame

from jeu.entites.bonus import BonusBouclier, Coeur
from jeu.entites.ennemis.boss import Boss
from jeu.entites.projectiles import ProjectileBarrage
from jeu.etat_partie import EtatPartie


@lru_cache(maxsize=16)
def _creer_halo_bouclier(largeur, hauteur):
    """Prépare le champ d'énergie transparent pour cette taille de sprite."""
    halo = pygame.Surface((largeur + 16, hauteur + 16), pygame.SRCALPHA)
    contour = halo.get_rect().inflate(-6, -6)

    pygame.draw.ellipse(halo, (28, 104, 229, 20), halo.get_rect(), 2)
    pygame.draw.ellipse(halo, (42, 140, 255, 55), contour.inflate(4, 4), 2)
    pygame.draw.ellipse(halo, (25, 117, 231, 40), contour)
    pygame.draw.ellipse(halo, (77, 202, 255, 200), contour, 1)
    pygame.draw.ellipse(halo, (77, 202, 255, 75), contour.inflate(-4, -4), 1)
    pygame.draw.arc(halo, (185, 249, 255, 255), contour, 0.58 * pi, 0.95 * pi, 2)
    pygame.draw.arc(halo, (185, 249, 255, 255), contour, 1.58 * pi, 1.95 * pi, 2)
    return halo


def _dessiner_bouclier(ecran, bouclier, rectangle):
    """Affiche le halo centré derrière le sprite si le bouclier est actif."""
    if bouclier is not None and bouclier.actif:
        halo = _creer_halo_bouclier(*rectangle.size)
        ecran.blit(halo, halo.get_rect(center=rectangle.center))


def dessiner_vaisseau(ecran, vaisseau, sprite):
    """Dessine le vaisseau et son bouclier actif.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param vaisseau: Vaisseau à dessiner.
    :type vaisseau: Vaisseau
    :param sprite: Image du vaisseau chargée au démarrage.
    :type sprite: pygame.Surface
    """
    rectangle = pygame.Rect(vaisseau.zone_collision())
    _dessiner_bouclier(ecran, vaisseau.bouclier, rectangle)
    ecran.blit(sprite, rectangle.topleft)

def dessiner_flotte(ecran, flotte, sprites):
    """Dessine chaque ennemi avec le sprite indiqué par son type.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param flotte: Formation d'ennemis.
    :type flotte: Flotte
    :param sprites: Sprites chargés, indexés par nom.
    :type sprites: dict[str, pygame.Surface]
    """
    for ennemi in flotte.ennemis:
        rectangle = pygame.Rect(ennemi.zone_collision())
        _dessiner_bouclier(ecran, ennemi.bouclier, rectangle)
        ecran.blit(sprites[ennemi.type_ennemi], rectangle.topleft)

def dessiner_avertissement_boss(ecran, flotte):
    """Trace les colonnes annoncées par le boss.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param flotte: Formation d'ennemis.
    :type flotte: Flotte
    """
    bas = ecran.get_height() - 1

    for ennemi in flotte.ennemis:
        if isinstance(ennemi, Boss):
            for x in ennemi.colonnes_barrage():
                pygame.draw.line(ecran, (255, 145, 70), (x, 0), (x, bas), 2)

def dessiner_projectile(ecran, projectile, sprites):
    """Affiche le sprite adapté au type et au sens du tir.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param projectile: Tir à dessiner.
    :type projectile: Projectile
    :param sprites: Sprites chargés, indexés par nom.
    :type sprites: dict[str, pygame.Surface]
    """
    if isinstance(projectile, ProjectileBarrage):
        nom = "tir_boss"
    else:
        nom = "tir_joueur" if projectile.direction < 0 else "tir_ennemi"
    x, y, _, _ = projectile.zone_collision()
    ecran.blit(sprites[nom], (x, y))


def dessiner_score(ecran, police, score):
    """Affiche le score du joueur.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param score: Score courant du joueur.
    :type score: int
    """
    texte = police.render(f"Score : {score}", True, (255,255,255))
    ecran.blit(texte, (15,15 ))

def dessiner_vies(ecran, police, vies):
    """Affiche le nombre de vies restantes.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param vies: Nombre de vies restantes.
    :type vies: int
    """
    texte = police.render(f"VIES : {vies}", True, (255, 255, 255))
    ecran.blit(texte, (15,37))

def dessiner_vague(ecran, police, niveau, ennemis_restants):
    """Affiche la vague et le nombre d'ennemis restants.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param niveau: Numéro de la vague en cours.
    :type niveau: int
    :param ennemis_restants: Nombre d'ennemis encore en jeu.
    :type ennemis_restants: int
    """
    blanc = (255, 255, 255)
    largeur = ecran.get_width()

    vague = police.render(f"VAGUE {niveau}", True, blanc)
    ennemis = police.render(f"ENNEMIS RESTANTS : {ennemis_restants}", True, blanc)

    ecran.blit(vague, vague.get_rect(midtop=(largeur // 2, 15)))
    ecran.blit(ennemis, ennemis.get_rect(topright=(largeur - 15, 15)))

def dessiner_bonus(ecran, bonus, sprites):
    """Dessine le sprite du bonus à la position de sa zone de collision.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param bonus: Bonus actif sur le terrain.
    :type bonus: Bonus
    :param sprites: Sprites des bonus indexés par nom.
    :type sprites: dict[str, pygame.Surface]
    """
    if isinstance(bonus, Coeur):
        sprite = sprites["coeur"]
    elif isinstance(bonus, BonusBouclier):
        sprite = sprites["bouclier"]
    else:
        return

    ecran.blit(sprite, (bonus.x, bonus.y))


def dessiner_mine(ecran, mine, sprites):
    """Dessine la mine et son rayon si elle est armée.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param mine: Mine à dessiner.
    :type mine: Mine
    :param sprites: Sprites chargés, indexés par nom.
    :type sprites: dict[str, pygame.Surface]
    """
    nom = "mine_armee" if mine.armee else "mine"
    if mine.armee:
        pygame.draw.circle(ecran, (255, 205, 85), mine.centre, mine.rayon_detection, 1)

    x, y, _, _ = mine.zone_collision()
    ecran.blit(sprites[nom], (x, y))


def dessiner_explosion_mine(ecran, explosion):
    """Trace le cercle correspondant au rayon de l'explosion.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param explosion: Couple contenant le centre et le rayon en pixels.
    :type explosion: tuple[tuple[int, int], int]
    """
    centre, rayon = explosion
    pygame.draw.circle(ecran, (255, 145, 70), centre, rayon, 3)

def dessiner_etat_mine(ecran, police, mine_active, ennemis_restants):
    """Indique si la mine est posée, prête ou en cours de recharge.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param mine_active: Indique si une mine est déjà posée.
    :type mine_active: bool
    :param ennemis_restants: Nombre d'ennemis à éliminer pour recharger
        la mine.
    :type ennemis_restants: int
    """
    if mine_active:
        texte = "MINE POSÉE"
    elif ennemis_restants == 0:
        texte = "MINE PRÊTE [X]"
    else:
        texte = f"MINE : ENCORE {ennemis_restants} À ÉLIMINER"

    image = police.render(texte, True, (255, 205, 85))
    position = image.get_rect(midtop=(ecran.get_width() // 2, 37))
    ecran.blit(image, position)

def dessiner_chrono(ecran, police, duree_secondes):
    """Affiche la durée écoulée au format minutes:secondes.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param duree_secondes: Temps écoulé en secondes entières.
    :type duree_secondes: int
    """
    minutes, secondes = divmod(duree_secondes, 60)
    texte = police.render(f"Temps : {minutes:02d}:{secondes:02d}", True, (255, 255, 255))
    position = texte.get_rect(topright=(ecran.get_width() - 15, 37))
    ecran.blit(texte, position)


def dessiner_compteurs_tirs(ecran, police, tirs_normaux, mines_lancees):
    """Affiche les nombres de tirs normaux et de mines utilisés.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param tirs_normaux: Nombre de tirs normaux utilisés.
    :type tirs_normaux: int
    :param mines_lancees: Nombre de mines lancées.
    :type mines_lancees: int
    """
    lignes = (f"Tirs utilisés : {tirs_normaux}", f"Mines utilisées : {mines_lancees}")
    droite = ecran.get_width() - 15

    for ligne, haut in zip(lignes, (59, 81)):
        texte = police.render(ligne, True, (255, 255, 255))
        ecran.blit(texte, texte.get_rect(topright=(droite, haut)))


def dessiner_partie(
    ecran, police, joueur, partie, sprite_vaisseau, sprites_ennemis,
    sprites_projectiles, sprites_bonus
):
    """Dessine le terrain et le tableau de bord.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param joueur: Vaisseau du joueur.
    :type joueur: Vaisseau
    :param partie: État de la partie à afficher.
    :type partie: Partie
    :param sprite_vaisseau: Image du vaisseau.
    :type sprite_vaisseau: pygame.Surface
    :param sprites_ennemis: Images indexées par type d'ennemi.
    :type sprites_ennemis: dict[str, pygame.Surface]
    :param sprites_projectiles: Images des tirs et de la mine.
    :type sprites_projectiles: dict[str, pygame.Surface]
    :param sprites_bonus: Images des bonus qui tombent sur le terrain.
    :type sprites_bonus: dict[str, pygame.Surface]
    """
    dessiner_avertissement_boss(ecran, partie.flotte)
    dessiner_vaisseau(ecran, joueur, sprite_vaisseau)
    dessiner_flotte(ecran, partie.flotte, sprites_ennemis)

    if partie.bonus is not None:
        dessiner_bonus(ecran, partie.bonus, sprites_bonus)
    if partie.mine is not None:
        dessiner_mine(ecran, partie.mine, sprites_projectiles)
    if partie.explosion_mine is not None:
        dessiner_explosion_mine(ecran, partie.explosion_mine)

    for projectile in partie.projectiles:
        dessiner_projectile(ecran, projectile, sprites_projectiles)

    for projectile in partie.projectiles_ennemis:
        dessiner_projectile(ecran, projectile, sprites_projectiles)

    dessiner_score(ecran, police, partie.score)
    dessiner_vies(ecran, police, joueur.vies)
    dessiner_vague(ecran, police, partie.niveau, len(partie.flotte.ennemis))

    if partie.etat == EtatPartie.EN_COURS:
        aide = police.render("Échap : menu", True, (220, 230, 245))
        ecran.blit(aide, aide.get_rect(bottomleft=(15, ecran.get_height() - 10)))
        dessiner_chrono(ecran, police, partie.duree_secondes())
        dessiner_compteurs_tirs(
            ecran, police, partie.tirs_normaux, partie.mines_lancees
        )

    dessiner_etat_mine(
        ecran, police, partie.mine is not None, partie.ennemis_avant_mine()
    )
