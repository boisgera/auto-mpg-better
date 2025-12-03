# auto-mpg v1 - Projet original

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

Par exemple : 

  - 📖 **Génération du PDF**. Si l'on connait un peu LaTeX, on peut supposer
    qu'il faut commencer par exécuter la commande `latex article.tex`. 
    Mais celle-ci génère l'erreur

    ```
    ! LaTeX Error: File `images/prediction.png' not found.

    See the LaTeX manual or LaTeX Companion for explanation.
    Type  H <return>  for immediate help.
    ...

    l.40 ...s[width=\textwidth]{images/prediction.png}
    ```

    Est-ce qu'une image est manquante ?

  - 🖥️ **Exécution du notebook.** De même, on peut reconnaître que l'extension
    du fichier `notebook.ipynb` caractérise un notebook Jupyter et donc 
    l'ouvrir avec la commande `jupyter lab notebook.ipynb`. Cela marche bien,
    mais à l'exécution on obtient :

    ```
    ---------------------------------------------------------------------------
    ModuleNotFoundError                       Traceback (most recent call last)
    Cell In[1], line 1
    ----> 1 import matplotlib.pyplot as plt
          2 import numpy as np
          3 import pandas as pd

    ModuleNotFoundError: No module named 'matplotlib'
    ```

    C'est donc a priori que Python et JupyterLab ne suffisent pas pour exécuter 
    le notebook ? Qu'il faut installer la bibliothèque `matplotlib` ? Mais
    dans quelle version ? Et quelle autre bibliothèque manque ?

 De façon plus générale, le projet actuel ne répond pas à ces questions :

  - 🏭 **Processus.** 
  
      - Est-ce que tous les fichiers sources nécessaires à la production des 
        artefacts sont bien présents ? 
        
      - Y'a-t'il une séquence précise d'étapes à suivre pour produire tous les 
        artefacts ?

  - 🖥️ **Logiciels.** 
  
      - Quelles sont les commandes à invoquer à chaque étape ? 
      
      - Quels logiciels nécessitent-elles ?
    
      - Dans quelle version ? 
      
      - Sur quelles plate-formes peut-on les exécuter ?