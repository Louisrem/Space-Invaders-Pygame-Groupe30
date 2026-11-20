"""Décrit la formation des ennemis et les bonus associés aux vagues."""

from .entites.bonus import BonusBouclier, Coeur

# Chaque numéro désigne une vague. Chaque chaîne représente une rangée.
# Les lettres viennent de CATALOGUE_ENNEMIS. Un point représente une case vide.
# Pour ajouter une vague, prends le numéro suivant et écris ses rangées.

VAGUES = {
    1: ("NNNNN", "NNNNN"),
    2: ("NNNNN", "NNNNN", "TTTTT"),
    3: ("NNNNN", "NNNNN", "T.T.T", ".R.R."),
    4: ("NNNNN", "NNNNN", "P.T.P", ".R.R."),
    5: ("..B..", "NNNNN", "P.T.P", ".R.R."),
}

# Associe un bonus à une vague. Par exemple, 2: Coeur prévoit un cœur en vague 2.
# Les vagues absentes de ce dictionnaire n’ont pas de bonus.
BONUS_PAR_VAGUE = {
    2: Coeur,
    3: BonusBouclier,
    4: Coeur,
}
