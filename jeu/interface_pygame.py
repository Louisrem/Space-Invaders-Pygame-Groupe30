import pygame
from jeu.ennemis.boss import Boss
from jeu.bonus import BonusBouclier, Coeur

def dessiner_vaisseau(ecran, vaisseau):
    rectangle = pygame.Rect(
        vaisseau.x, vaisseau.y, vaisseau.largeur, vaisseau.hauteur
    )
    pygame.draw.rect(ecran,(80,220,160), rectangle)
    if vaisseau.bouclier is not None and vaisseau.bouclier.actif:
        pygame.draw.rect(ecran, (80, 190, 255), rectangle, 2)

def dessiner_flotte(ecran, flotte):
    for ennemi in flotte.ennemis:
        rectangle = pygame.Rect(
            ennemi.x, ennemi.y, ennemi.largeur, ennemi.hauteur
        )
        couleur = (180, 105, 255) if isinstance(ennemi, Boss) else (240, 100, 100)
        pygame.draw.rect(ecran, couleur, rectangle)
        if ennemi.bouclier is not None and ennemi.bouclier.actif:
            pygame.draw.rect(ecran, (80,190,255), rectangle, 2)

def dessiner_avertissement_boss(ecran, flotte):
    bas = ecran.get_height() - 1

    for ennemi in flotte.ennemis:
        if isinstance(ennemi, Boss):
            for x in ennemi.colonnes_barrage():
                pygame.draw.line(ecran, (255, 145, 70), (x, 0), (x, bas), 2)

def dessiner_projectile(ecran, projectile):
    rectangle = pygame.Rect(projectile.zone_collision())
    pygame.draw.rect(ecran, (255,255,255), rectangle)

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

def dessiner_message_centre(ecran, police, texte):
    message = police.render(texte, True, (255, 255, 255))
    position = message.get_rect(center=ecran.get_rect().center)
    ecran.blit(message, position)

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


def dessiner_mine(ecran, mine):
    couleur = (255, 205, 85) if mine.armee else (206, 160, 65)
    if mine.armee:
        pygame.draw.circle(ecran, couleur, mine.centre, mine.rayon_detection, 1)
    pygame.draw.circle(ecran, couleur, mine.centre, mine.largeur // 2)


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

def dessiner_menu(ecran, police):
    ecran.fill((0, 0, 0))
    centre_x, centre_y = ecran.get_rect().center

    titre = police.render("SPACE INVADERS", True, (255, 255, 255))
    ecran.blit(titre, titre.get_rect(center=(centre_x, centre_y - 40)))

    dessiner_message_centre(ecran, police, "Entrée pour jouer")