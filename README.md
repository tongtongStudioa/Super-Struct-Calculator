# Super-Struct-Calculator
A student project to understand different type of concept in engineer structure course.

# Project structure
Super-struct-calculator/
├── steel_section/
│   ├── __init__.py
│   ├── main.py             # Point d'entrée du programme
│   ├── calculations/       # Module contenant les calculs spécifiques
│   │   ├── __init__.py
│   │   ├── bending.py      # Calculs de moment fléchissant
│   │   ├── shear.py        # Calculs de cisaillement
│   │   ├── deflection.py   # Calculs des flèches
│   ├── utils/              # Module pour les fonctions utilitaires
│   │   ├── __init__.py
│   │   ├── validators.py   # Validation des entrées utilisateur
│   │   ├── file_handler.py # Gestion des fichiers d'entrée/sortie
│   ├── config.py           # Paramètres globaux et constantes
│   ├── eurocode_constants.py  # Valeurs et coefficients spécifiques à l'Eurocode
├── tests/                  # Tests unitaires
│   ├── test_bending.py
│   ├── test_shear.py
├── requirements.txt        # Liste des dépendances
├── README.md               # Documentation du projet
├── .gitignore              # Exclusion des fichiers non nécessaires
