# auto-mpg

Que penser du projet initial ?

  - 👍 Un article au format PDF est fourni, ainsi que ses sources 
    (`article.tex` et `article.bib`)
  
  - 👍 L'article donne le modèle prédictif utilisé 
    (structure et poids) et ses performances; 
    ses prédictions sont également illustrées graphiquement.

  - 👍 Un notebook Jupyter (`notebook.ipynb`) détaille et illustre la 
    méthodologie d'apprentissage utilisée.
  

Mais nous sommes tout de suite confrontés à des difficultés si nous essayons
de reproduire les artefacts du projet 
(ici l'article en PDF et les résultats du notebook) 
par nous-mêmes. 

Par example, on peut supposer que pour générer le PDF il faudra 
exécuter la commande `latex article.tex`. Mais celle-ci génère l'erreur

```
! LaTeX Error: File `images/prediction.png' not found.

See the LaTeX manual or LaTeX Companion for explanation.
Type  H <return>  for immediate help.
 ...

l.40 ...s[width=\textwidth]{images/prediction.png}
```

De même en exécutant le notebook ouvert avec `jupyter lab notebook.ipynb`,
j'obtiens

```
---------------------------------------------------------------------------
ModuleNotFoundError                       Traceback (most recent call last)
Cell In[1], line 1
----> 1 import matplotlib.pyplot as plt
      2 import numpy as np
      3 import pandas as pd

ModuleNotFoundError: No module named 'matplotlib'
```

C'est donc que Python et JupyterLab ne suffisent pas pour exécuter le notebook ?

Est-ce qu'une image est manquante ? De façon plus générale :

  - Est-ce que tous les fichiers sources nécessaires à la production des 
    artefacts sont présents ? Y'a-t'il une séquence bien précise 
    d'étapes à suivre pour produire tous les artefacts ?

  - Quelles sont les commandes à invoquer ? Quels logiciels nécessitent-elles ?
    Sur quelles plate-formes peut-on les exécuter ?