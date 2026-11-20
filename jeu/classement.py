"""Lit et enregistre les résultats dans le classement local JSON."""

import json
from pathlib import Path

FICHIER_CLASSEMENT = Path(__file__).resolve().parent.parent / "classement.json"

def lire_resultats():
    """Lit les résultats enregistrés dans l'ordre des parties jouées.

    :return: Les résultats, ou une liste vide si le fichier n'existe
        pas.
    :rtype: list[dict]
    """
    if not FICHIER_CLASSEMENT.exists():
        return []

    return json.loads(FICHIER_CLASSEMENT.read_text(encoding="utf-8"))


def meilleurs_resultats():
    """Renvoie au plus cinq résultats par score décroissant.

    À score égal, conserve l'ordre d'enregistrement.

    :return: Jusqu'à cinq résultats du classement local.
    :rtype: list[dict]
    """
    return sorted(lire_resultats(), key=lambda resultat: resultat["score"], reverse=True)[:5]


def enregistrer_resultat(resultat):
    """Ajoute le résultat d'une partie au classement local.

    Écrit la liste dans un fichier temporaire avant de remplacer le
    JSON.

    :param resultat: Dictionnaire produit par Partie.resultat().
    :type resultat: dict
    """
    resultats = lire_resultats()
    resultats.append(resultat)

    contenu = json.dumps(resultats, ensure_ascii=False, indent=4)
    fichier_temporaire = FICHIER_CLASSEMENT.with_suffix(".json.tmp")
    fichier_temporaire.write_text(contenu, encoding="utf-8")
    fichier_temporaire.replace(FICHIER_CLASSEMENT)
