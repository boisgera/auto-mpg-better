# auto-mpg v4 –⁠ Bibliographie et jeu de données

Le projet initial contenait un fichier de bibliographie `references.bib`
au format BibTeX

```bibtex
@misc{auto_mpg_9,
  author       = {Quinlan, R.},
  title        = {{Auto MPG}},
  year         = {1993},
  howpublished = {UCI Machine Learning Repository},
  doi          = {10.24432/C5859H},
}
```

Avec le DOI qu'il comporte, on peut retrouver la page actuelle 
`https://archive.ics.uci.edu/dataset/9/auto+mpg` consacrée
au jeu de données. 
En fouillant un peu, on trouve ensuite le lien vers le jeu de données lui-même 
`https://archive.ics.uci.edu/static/public/9/data.csv`.

Mettons un peu d'ordre dans tout cela !

## Bibliographie augmentée

On peut réécrire le fichier BibTex au format CSL-JSON (que savent gérer Pandoc,
Zotero, etc.), qui sera plus facile à exploiter de façon programmatique.
On en profit pour ajouter l'information que nous avons du rechercher, l'URL
d'accès direct au jeux de données. Pour nous assurer de l'intégrité du jeu
de données, on peut aussi calculer une somme de contrôle (*checksum*) de ces
données et l'ajouter dans les attributs personnalisés de notre bibliographie.

```json
[
  {
    "id": "auto_mpg_9",
    "title": "Auto MPG",
    "type": "dataset",
    "author": [
      {
        "family": "Quilan",
        "given": "John Ross"
      }
    ],
    "issued": {
      "date-parts": [[1993]]
    },
    "accessed": {
      "date-parts": [[2025, 3, 1]]
    },
    "archive": "UCI Machine Learning Repository",
    "DOI": "10.24432/C5859H",
    "URL": "https://archive.ics.uci.edu/static/public/9/data.csv",
    "custom": {
      "checksum": {
        "value": "ca25194200142eb13650f02ec2d64980",
        "type": "md5"
      }
    }
  }
]
```

On en profite pour ranger ce fichier dans un sous-dossier dédié `bibliography`
et de le compléter par une tâche `bibliography` qui génère un format BibTeX 
associé (si nécessaire !).

## Gestion des données

Cf. [la section dédiée](datasets).



