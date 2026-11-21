"""Affichage du terrain, des objets et du tableau de bord."""

import pygame

from jeu.entites.bonus import BonusBouclier, Coeur
from jeu.entites.ennemis.boss import Boss
from jeu.entites.projectiles import ProjectileBarrage
from jeu.etat_partie import EtatPartie


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
    ecran.blit(sprite, rectangle.topleft)
    if vaisseau.bouclier is not None and vaisseau.bouclier.actif:
        pygame.draw.rect(ecran, (80, 190, 255), rectangle, 2)

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
        ecran.blit(sprites[ennemi.type_ennemi], rectangle.topleft)
        if ennemi.bouclier is not None and ennemi.bouclier.actif:
            pygame.draw.rect(ecran, (80,190,255), rectangle, 2)

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
        dessiner_chrono(ecran, police, partie.duree_secondes())
        dessiner_compteurs_tirs(
            ecran, police, partie.tirs_normaux, partie.mines_lancees
        )

    dessiner_etat_mine(
        ecran, police, partie.mine is not None, partie.ennemis_avant_mine()
    )
