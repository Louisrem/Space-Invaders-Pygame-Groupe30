from enum import Enum

class EtatPartie(Enum):
    MENU = "menu"
    EN_COURS = "en_cours"
    PAUSE = "pause"
    VICTOIRE = "victoire"
    DEFAITE = "defaite"