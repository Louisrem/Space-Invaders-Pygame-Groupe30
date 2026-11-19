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