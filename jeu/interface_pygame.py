import pygame
from jeu.ennemis.boss import Boss

def dessiner_vaisseau(ecran, vaisseau):
    rectangle = pygame.Rect(
        vaisseau.x, vaisseau.y, vaisseau.largeur, vaisseau.hauteur
    )
    pygame.draw.rect(ecran,(80,220,160), rectangle)

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

def dessiner_defaite(ecran, police):
    message = police.render("PARTIE TERMINÉE", True, (255, 255, 255))
    position = message.get_rect(center=ecran.get_rect().center)
    ecran.blit(message, position)