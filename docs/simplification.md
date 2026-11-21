# Ce qui change par rapport à la version complète

Cette version garde tout ce que demande la Partie 1 et retire le reste.
Le code passe d'environ 1 800 à 800 lignes (docstrings comprises).

## Retiré

- Le tir de barrage du boss (annonce des colonnes, lignes orange, son).
- Les ennemis « rapide » et « protégé » (et donc les deux groupes de la flotte).
- Les bonus (cœur, bouclier) et la classe `Bouclier`.
- Le classement JSON, le chrono, les compteurs de tirs, la pause et l'écran classement.
- La recharge de la mine (5 éliminations) : une seule mine à la fois suffit.
- Les vagues 4 et 5 (il en reste 3, le boss est dans la dernière).
- `docs/guide_extension.md` : le README contient l'essentiel.
- Les sous-dossiers `entites/` et `entites/ennemis/` : 22 fichiers Python ramenés à 12
  (un fichier par idée du jeu, deux paquetages `jeu/` et `interface/`).

## Amélioré

- **Classe mère `Entite`** : `Vaisseau`, `Ennemi` et `Projectile` en héritent
  (position, taille, `zone_collision()`, `touche()`). Le test de collision
  est rangé avec elle dans `entite.py`.
- **Armes polymorphes** : `Partie.tirer(type_projectile)` accepte n'importe
  quelle sous-classe de `Projectile`. Chaque arme décide elle-même des ennemis
  qu'elle touche (`ennemis_touches()`). Ajouter une arme ne demande plus de
  modifier `Partie`.
- **Boss polymorphe** : `Boss` redéfinit `subir_impact()` et tire plus vite
  dès qu'il est blessé. `Tireur` est aussi une sous-classe d'`Ennemi`.
- **Aucun nom d'image dans `jeu/`** : c'est `interface/affichage.py` qui
  associe chaque classe à son image (`IMAGES`, `nom_image()`). Une nouvelle
  sous-classe sans image prend celle de sa classe mère (parcours du `__mro__`).
- **Encapsulation** (cours 04) : `vies`, `pv`, la position `x`/`y` des entités
  (modifiée seulement par `decaler()`), et tout l'état de `Partie`
  (`score`, `etat`, `niveau`, `flotte`, `joueur`, listes de tirs) sont en
  lecture seule avec `@property` ; les listes sont rendues en tuple pour
  qu'on ne puisse pas les modifier de l'extérieur.
- **Flotte itérable** (cours 06) : `__iter__` (générateur avec `yield from`) et
  `__len__`, donc `for ennemi in flotte` et `len(flotte)`.
- **La partie possède le vaisseau** (composition) : `main.py` ne fait plus que
  transmettre les touches.
- **`__repr__` et `__str__`** (cours 3, labo 3) : `print(boss)` affiche
  `Boss(x=218, y=60, pv=3)` et `print(partie)` affiche `Vague 1 · score 0 · 3 vies`.
- **Couverture des tests** : environ 98 % de `jeu/`, commande dans le README.
- **Pas de nombres magiques** : la grille de la flotte, la hauteur du vaisseau,
  sa vitesse et les images par seconde sont des constantes nommées.
- **Événements sans fichiers** : `EvenementPartie` ne connaît pas les fichiers
  WAV (`auto()`), c'est `interface/sons.py` qui choisit le son. Le tir ennemi a
  son propre événement (`TIR_ENNEMI`).
- **Score** : chaque ennemi a ses `POINTS` (1, et 5 pour le boss).
- **README** : installation avec `venv` et `pip`, sans outil supplémentaire.

## Exigences de la Partie 1

| Exigence | Où |
| --- | --- |
| Déplacer un vaisseau et tirer | `Vaisseau`, `Partie.tirer()` |
| Flotte de plusieurs ennemis | `Flotte`, `vagues.py` |
| 2 types d'ennemis ou plus | `Ennemi`, `Tireur(Ennemi)`, `Boss(Ennemi)` à 3 PV |
| 2 types d'armes ou plus | `Projectile`, `Mine(Projectile)` |
| Collisions et score | `Entite.touche()` (entite.py), `Partie.score` |
| Héritage | `Entite` → `Vaisseau`, `Ennemi`, `Projectile` ; `Tireur(Ennemi)`, `Boss(Ennemi)`, `Mine(Projectile)`, `SansTir`/`TirSimple(ComportementTir)` |
| Composition | `Partie` → `Flotte`, `Vaisseau` ; `Ennemi` → `ComportementTir` |
| Polymorphisme | `tirer()`, `ennemis_touches()`, `Boss.subir_impact()` |
| Logique séparée de l'affichage | `jeu/` n'importe jamais Pygame et ne connaît aucune image |
| Modules et paquetages | paquetages `jeu/` (9 modules) et `interface/` (2 modules) |
