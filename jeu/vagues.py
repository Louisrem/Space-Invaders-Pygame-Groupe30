"""Décrit la formation des ennemis de chaque vague."""

# Chaque numéro désigne une vague. Chaque chaîne représente une rangée.
# Les lettres viennent de CATALOGUE_ENNEMIS. Un point représente une case vide.
# Pour ajouter une vague, prends le numéro suivant et écris ses rangées.
VAGUES = {
    1: ("NNNNN", "NNNNN"),
    2: ("NTNTN", "NNNNN"),
    3: ("..B..", "TNTNT", "NNNNN"),
}
