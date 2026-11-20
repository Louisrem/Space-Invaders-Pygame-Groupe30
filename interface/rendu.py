import pygame

from jeu.entites.bonus import BonusBouclier, Coeur
from jeu.entites.ennemis.boss import Boss
from jeu.entites.projectiles import ProjectileBarrage
from jeu.etat_partie import EtatPartie


def dessiner_vaisseau(ecran, vaisseau, sprite):
    rectangle = pygame.Rect(vaisseau.zone_collision())
    ecran.blit(sprite, rectangle.topleft)
    if vaisseau.bouclier is not None and vaisseau.bouclier.actif:
        pygame.draw.rect(ecran, (80, 190, 255), rectangle, 2)

def dessiner_flotte(ecran, flotte, sprites):
    for ennemi in flotte.ennemis:
        rectangle = pygame.Rect(ennemi.zone_collision())
        ecran.blit(sprites[ennemi.type_ennemi], rectangle.topleft)
        if ennemi.bouclier is not None and ennemi.bouclier.actif:
            pygame.draw.rect(ecran, (80,190,255), rectangle, 2)

def dessiner_avertissement_boss(ecran, flotte):
    bas = ecran.get_height() - 1

    for ennemi in flotte.ennemis:
        if isinstance(ennemi, Boss):
            for x in ennemi.colonnes_barrage():
                pygame.draw.line(ecran, (255, 145, 70), (x, 0), (x, bas), 2)

def dessiner_projectile(ecran, projectile, sprites):
    if isinstance(projectile, ProjectileBarrage):
        nom = "tir_boss"
    else:
        nom = "tir_joueur" if projectile.direction < 0 else "tir_ennemi"
    x, y, _, _ = projectile.zone_collision()
    ecran.blit(sprites[nom], (x, y))


def dessiner_score(ecran, police, score):
    texte = police.render(f"Score : {score}", True, (255,255,255))
    ecran.blit(texte, (15,15 ))

def dessiner_vies(ecran, police, vies):
    texte = police.render(f"VIES : {vies}", True, (255, 255, 255))
    ecran.blit(texte, (15,37))

def dessiner_vague(ecran, police, niveau, ennemis_restants):
    blanc = (255, 255, 255)
    largeur = ecran.get_width()

    vague = police.render(f"VAGUE {niveau}", True, blanc)
    ennemis = police.render(f"ENNEMIS RESTANTS : {ennemis_restants}", True, blanc)

    ecran.blit(vague, vague.get_rect(midtop=(largeur // 2, 15)))
    ecran.blit(ennemis, ennemis.get_rect(topright=(largeur - 15, 15)))

def dessiner_coeur(ecran, coeur):
    x, y = coeur.x, coeur.y
    rose = (255, 90, 130)
    pygame.draw.circle(ecran, rose, (x + 6, y + 6), 6)
    pygame.draw.circle(ecran, rose, (x + 18, y + 6), 6)
    pygame.draw.polygon(
        ecran, rose, [(x, y + 7), (x + 23, y + 7), (x + 12, y + 23)]
    )

def dessiner_bonus(ecran, bonus):
    if isinstance(bonus, Coeur):
        dessiner_coeur(ecran, bonus)
    elif isinstance(bonus, BonusBouclier):
        rectangle = pygame.Rect(bonus.zone_collision())
        pygame.draw.rect(ecran, (80, 190, 255), rectangle, 3)


def dessiner_mine(ecran, mine, sprites):
    nom = "mine_armee" if mine.armee else "mine"
    if mine.armee:
        pygame.draw.circle(ecran, (255, 205, 85), mine.centre, mine.rayon_detection, 1)

    x, y, _, _ = mine.zone_collision()
    ecran.blit(sprites[nom], (x, y))


def dessiner_explosion_mine(ecran, explosion):
    centre, rayon = explosion
    pygame.draw.circle(ecran, (255, 145, 70), centre, rayon, 3)

def dessiner_etat_mine(ecran, police, mine_active, ennemis_restants):
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
    minutes, secondes = divmod(duree_secondes, 60)
    texte = police.render(f"Temps : {minutes:02d}:{secondes:02d}", True, (255, 255, 255))
    position = texte.get_rect(topright=(ecran.get_width() - 15, 37))
    ecran.blit(texte, position)


def dessiner_compteurs_tirs(ecran, police, tirs_normaux, mines_lancees):
    lignes = (f"Tirs utilisés : {tirs_normaux}", f"Mines utilisées : {mines_lancees}")
    droite = ecran.get_width() - 15

    for ligne, haut in zip(lignes, (59, 81)):
        texte = police.render(ligne, True, (255, 255, 255))
        ecran.blit(texte, texte.get_rect(topright=(droite, haut)))


def dessiner_partie(
    ecran, police, joueur, partie, sprite_vaisseau, sprites_ennemis, sprites_projectiles
):
    dessiner_avertissement_boss(ecran, partie.flotte)
    dessiner_vaisseau(ecran, joueur, sprite_vaisseau)
    dessiner_flotte(ecran, partie.flotte, sprites_ennemis)

    if partie.bonus is not None:
        dessiner_bonus(ecran, partie.bonus)
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
