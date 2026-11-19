import pygame

def main():
    pygame.display.init()
    pygame.display.set_mode((800,600))
    pygame.display.set_caption("Space Invaders - Groupe 30")

    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()

if __name__ == "__main__":
    main()

