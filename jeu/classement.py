import json
from pathlib import Path

FICHIER_CLASSEMENT = Path(__file__).resolve().parent.parent / "classement.json"

def lire_resultats():
    if not FICHIER_CLASSEMENT.exists():
        return []

    return json.loads(FICHIER_CLASSEMENT.read_text(encoding="utf-8"))


def meilleurs_resultats():
    return sorted(lire_resultats(), key=lambda resultat: resultat["score"], reverse=True)[:5]


def enregistrer_resultat(resultat):
    resultats = lire_resultats()
    resultats.append(resultat)

    contenu = json.dumps(resultats, ensure_ascii=False, indent=4)
    fichier_temporaire = FICHIER_CLASSEMENT.with_suffix(".json.tmp")
    fichier_temporaire.write_text(contenu, encoding="utf-8")
    fichier_temporaire.replace(FICHIER_CLASSEMENT)
