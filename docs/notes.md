**Problème 1 :** Incompatibilité entre Python 3.14 et pygame 2.6.1 sur MacOS

**Quand ?** Lors de la création de l'environnement virtuel (`uv venv`) et de l'installation des dépendances (`uv pip install pygame`)
**Pourquoi ?** uv utilise Python 3.14 par défaut, pour lequel pygame 2.6.1 n'a pas encore de version précompilée sur macOS

**--> C'est pour ça qu'on va forcer Python 3.12**

**Problème 2 :** SyntaxWarning lors de l'exécution de `main.py`(`is` au lieu de `==`)

**Quand ?** Lors du lancement du jeu.
**Où ?** main.py, lignes 121 et 177 --> `if bullet_state is "ready":`ou `is "fire":`
**Erreur :** `SyntaxWarning: "is" with 'str' literal. Did you mean "=="?`

**Pourquoi ?**

* `is` = opérateur d'identité qui vérifie si 2 variables pointent vers le même emplacement de mémoire
* `==` compare la valeur du texte.

Python émet un avertissement car `is` sur du texte fonctionne par hasard (si Python réutilise la même case mémoire) mais peut échouer si une nouvelle chaîne identique est créée ailleurs. Après recherche, Python utilise une optimisation interne (*string interning*) : pour les mots courts écrits dans le code (comme "ready"), il ne crée souvent qu'une seule boîte et fait pointer les deux variables dessus. `is` renvoie `True` par pur hasard.

C'est d'ailleurs un défaut de conception si on fait POO. Car le programme ne crée qu'une seule fois les variables pour la position de la balle (`bulletX` et `bulletY`). Il n'y a pas de liste donc on peut ya voir qu'une seule fois les coordonnées X et Y. Lorsqu'on appuie une fois sur espace

```python
if bullet_state is "ready":
    bulletX = playerX
    fire_bullet(bulletX, bulletY)
```

La balle part vers le haut et bullet_state vaut "fire". Mais si on rappuie directement après sur Espace (alors que la première balle est tjrs en route). Comme bullet_state vaut "fire" et pas "ready", la condition est fausse du coup le bloc est ignoré. Si on supprimait le if, la nouvelle balle écraserait l'ancienne. Donc avec ce code, il est impossible d'avoir 2 balles visibles car 1 seul emplacement de mémoire.

DONC ! Si on veut ajouter des ennemis qui tirent, on est bloqué. Il faudrait une liste d'objets "tirs" par exemple. Et si on veut garder la règle "1 tir à la fois", on définira la règle aux entités concernées.

**Solution :**

- **Correction syntaxique :** Toujours utiliser `==` pour comparer des valeurs textuelles et réserver `is` aux comparaisons d'identité (`None`, `True`, `False`).
- **Refonte POO :** Supprimer les variables globales `bullet_state`, `bulletX` et `bulletY`. Créer une classe `Tir` (avec ses propres attributs `x`, `y`, `speed`, `owner`) et stocker les tirs actifs dans une liste (`Tirs = []`). La règle « 1 tir à la fois » devient alors une simple condition propre au joueur (`len(player_tirs) < 1`), ce qui permet aussi d'ajouter des tirs ennemis ou des armes multiples sans modifier la boucle principale.

**Problème 3** : Le jeu continue de tourner après le Game Over

**Quand ?** : Lorsqu'un ennemi touche le bas de l'écran.
Où ? : `main.py` (boucle principale `while running:`)

```python
# Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
```

**Pourquoi ?** Il n'y aucune séparation entre les états. (`MENU`,`PLAYING`,`PAUSE`, ...)
Lorsqu'un ennemi franchit la limite basse, tous les ennemis sont téléportés hors de l'écran (`enemyY[j] = 2000`) et d'afficher GAME OVER, mais la boucle continue, on peut toujours déplacer le vaisseau, et on entend toujours le son. Mais impossible de relancer.

**Solution possible** :

Ajouter une variable pour l'état du jeu dans la classe principale du jeu pour indiquer à quel phase le joueur se trouve.

**Problème 4 concernant les ennemis** : La gestion/création des ennemis

**Le code pour la création des ennemis**

```python
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
```

**Problème 4.1.**

Au lieu d'un seul objet par ennemi, on se retrouve avec 5 listes différentes pour stocker les caractéristiques relatives aux ennemis. Les données d'un seul ennemi sont éparpilées et le seul lien qui relie les caractéristiques à l'ennemi est son indice `[i]`. Mais du coup, si on veut insérer ou supprimer un ennemi, on risque de tout décaler et de mélanger les caractéristiques entre-elles. C'est difficile et fragile à maintenir.

**Solution possible 4.1.**

On peut créer une classe `Ennemi` (et des filles si on veut des types différents), ainsi toutes les caractéristiques d'un ennemi sont regroupées dans un seul objet. Du coup, on a plus qu'une liste d'objets `ennemis` à gérer. Si j'en ajoute 1 ou supprime 1 , tout sera synchronisé (sans décalage)

**Le code concernant la gestion des ennemis (collision)**

```python
# Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
```

**Problème 4.2**

Lorsqu'il y a une collision, au lieu de détruire l'ennemi, le programme change juste les coordonnées pour le téléporter plus haut. Déjà le tirage au sort propose y jusqu'à 150 (ce qui est très bas), et comme il n'est jamais supprimé, le nombre d'ennemis reste figé à 6. Donc il n'y a pas de fin

**Solution possible 4.2.**

Grâce à la liste d'objets `ennemis`, on n'est plus bloqué avec 6 emplacements fixes. Lorsqu'un ennemi est touché, on le supprime réellement de la liste (`ennemis.remove(ennemi)`) au lieu de le téléporter. Une fois que la liste est vide, on peut alors déclencher une victoire ou générer proprement une nouvelle vague d'ennemis positionnés tout en haut de l'écran.

**Le code concernant le déplacement de l'ennemi**

```python
 # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

```

**Problème 4.3**

Pour avancer, le programme utilise `enemyX[i] += enemyX_change[i]`(initialisé à 4), donc ici l'ennemi avance vers la droite (+4 px horizontalement).

Lorsque l'ennemi atteint le bord droite (736 px) `enemyX_change[i]` passe à -4 et l'ennemi repart vers la gauche et Y augmente de 40 (donc descend de 40px). Lorsqu'il touche le bord gauche, `enemyX_change[i]` passe à 4 et il avance vers la droite et Y augmente de 40 (donc descend aussi)

De plus, au départ, les ennemis apparaissent à des positions aléatoires (ne sont donc pas alignés en grille, comme dans le vrai Space Invaders). Chacun gère donc son propre déplacement (avec `enemyX_change`). Ainsi, dés qu'un ennemi atteint un bord, seulement cet ennemi inverse sa direction et descend. En prenant en compte que l'ennemi ne meurt part s'il est touché et réapparait aléatoirement, le groupe est totalement désynchronisé et les ennemis se croisent. Normalement, le groupe devrait former un bloc, si un seul ennemi touche un bord, c'est tout le groupe qui descend et change de direction en même temps. --> Pas de chevauchement et synchronisé.

**Solution possible 4.3.**

Placer les ennemis en grille en haut de l'écran au début de chaque vague, et centraliser la direction horizontale (`direction = 1` ou `-1`) pour tout le groupe. À chaque tour, tous les ennemis avancent ensemble dans la même direction. Ainsi, dès que l'un d'entre eux atteint un bord de l'écran, tout le bloc descend d'un cran et inverse son sens de déplacement en même temps. Concrètement, l'idée serait de passer d'un comportement individuel à un comportement de groupe avec une classe
