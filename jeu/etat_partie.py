"""États utilisés pour contrôler le déroulement d'une partie."""

from enum import Enum

class EtatPartie(Enum):
    """Énumère les états disponibles pour une partie."""
    MENU = "menu"
    EN_COURS = "en_cours"
    PAUSE = "pause"
    VICTOIRE = "victoire"
    DEFAITE = "defaite"