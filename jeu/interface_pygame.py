import pygame

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
        pygame.draw.rect(ecran,(240,100,100), rectangle)

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