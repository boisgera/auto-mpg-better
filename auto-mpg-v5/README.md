# auto-mpg v5 –⁠ Résultats : modèle et performance

Jusqu'à la version 4 du projet :

  - Les résultats produits dans l'étude doivent être reportés à la main dans 
    l'article `article.md` ; on doit également vérifier manuellement que les 
    informations de performance du modèle annoncées dans l'article sont vraies.

    En pratique, on peut passer beaucoup de temps à affiner les méthodes 
    de l'étude et donc faire change ses résultats. Est-ce que l'on va vraiment
    avoir le courage de synchroniser l'article à chaque fois? Est-ce qu'à force
    de répéter cette tâche répétitive on ne risque pas d'introduire des erreurs 
    de report ? 

  - On ne fait pas d'effort spécifique pour que l'utilisateur puisse utiliser
    facilement le modèle que l'on a produit : celui-ci doit a priori extraire 
    de l'article (ou mieux du notebook) la structure de notre modèle et ses 
    valeurs et les intégrer à ses propres expériences.

    Cela est très raisonnable ici compte tenu de la très grande simplicité de
    notre modèle et du tout petit jeu de valeurs impliquées. 
    Mais qu'en serait-il si sa structure était plus complexe ou qu'il 
    dépendait de quelques milliards de valeurs ?

  
## Améliorations

  - Nous rassemblons dans le notebook une structure de résultats contenant
    les grandeurs significatives produites dans l'étude qui décrivent
    le modèle ainsi que la distribution de son erreur de prédiction :

    ```json
    {
      "model": {
        "weight": 0.008990742553479284,
        "bias": -0.8944169922348109
      },
      "error": {
        "mean": 9.053982053881889e-15,
        "std": 1.8218352304345888
      }
    }
    ```

    Nous exportons ce jeu de résultats dans un fichier `models/results.json`.
    Le format JSON est à la fois lisible et très facile à exploiter de façon
    programmatique dans la plupart des contextes.

  - Nous remplaçons `article.md` par un fichier patron `article.md.j2` où
    certaines des valeurs, au lieu d'être écrites une fois pour toutes,
    sont des variables, repérables par les "moustaches" `{{ }}`. Par exemple
    dans le fragment

    ```markdown
    The numerical values of the model parameters are

    - slope: ${{ slope }}$
    - intercept: ${{ intercept }}$
    ```

    `slope` et `intercept` sont des variables. Exécuter la nouvelle commande

    ```
    pixi run article
    ```

    se chargera d'extraire les grandeurs pertinentes du fichier des résultats
    et de les injecter dans le patron d'article pour produire `article.md`.
    Au passage, nous pouvons vérifier que les performances minimales 
    promises dans l'article sont tenues, ou générer une erreur !

  - Pour faciliter l'exploitation du modèle, nous l'exportons au
    format [ONNX] (Open Neural Network Exchange), un format d'échange ouvert
    supporté par de nombreuses plate-formes d'exécution de modèles.
    
    Le fichier qui en résulte est `models/lp100.onnx`.

    Nous fournissons dans le notebook un exemple minimal utilisant
    la bibliothèque `onnxruntime` qui montre comment l'exploiter :

    ```python
    import onnxruntime as ort

    ONNX_PATH = "models/lp100.onnx"

    class ONNX_LP100:
        def __init__(self):
            self.session = ort.InferenceSession(ONNX_PATH)
        def __call__(self, weight_kg):
            input_shape = np.shape(weight_kg)
            input_is_scalar = np.isscalar(weight_kg)
            weight_kg = np.reshape(weight_kg, (-1, 1))
            lp100 = self.session.run(["lp100"], {"weight_kg": weight_kg})
            lp100 = np.reshape(lp100, input_shape)
            if input_is_scalar:
                lp100 = lp100.item()
            return lp100

    onnx_lp100 = ONNX_LP100()  

    onnx_lp100(weight_kg=1000.0) # output: 8.096325561244473
    ```

    ... mais cela devrait n'être qu'une formalité pour un chercheur ou ingénieur
    du domaine !
   
## Et si ?

Dans notre solution, les utilisateurs refont tourner l'algorithme 
d'apprentissage sur leur machine et produisent leur propre version
du modèle. Et si 

  - cette phase d'apprentissage était très longue ?
  
  - demandait des machines puissantes (mémoire, CPU, etc.) ?
  
  - produisant un très gros modèle ?

Comment simplifieriez-vous la vie à vos potentiels utilisateurs ?



[ONNX]: https://onnx.ai/