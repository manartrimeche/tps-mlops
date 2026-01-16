# TP MLOps : Versionnement de Données avec DVC

## Présentation du Projet

Ce dépôt illustre la mise en œuvre d’un workflow MLOps axé sur le versionnement de données à l’aide de DVC (Data Version Control) et l’utilisation de MinIO comme stockage S3 local. Le jeu de données Iris est utilisé pour démontrer la traçabilité, la reproductibilité et la synchronisation des artefacts de données dans un environnement contrôlé.

## Objectifs Techniques

- Déployer un stockage S3 local via MinIO
- Initialiser et configurer DVC pour le suivi des données
- Assurer la synchronisation entre le cache local et le stockage distant
- Garantir la reproductibilité des workflows de données

## Prérequis

- Git
- DVC (`pip install dvc[s3]`)
- Docker & Docker Compose
- Python 3.x

## Installation et Configuration

1. Cloner le dépôt :

   ```bash
   git clone <url-du-repo>
   cd mlops-dvc-iris
   ```

2. Démarrer MinIO :

   ```bash
   docker-compose up -d
   ```

   Accès : http://localhost:9001 (identifiants par défaut dans le compose)

3. Configurer les variables d’environnement pour DVC :

   ```powershell
   $env:AWS_ACCESS_KEY_ID="minio"
   $env:AWS_SECRET_ACCESS_KEY="minio12345"
   ```

4. Vérifier la configuration du remote DVC dans `.dvc/config`.

## Structure du Répertoire

```
mlops-dvc-iris/
├── data/raw/iris.csv          # Données Iris
├── data/raw/iris.csv.dvc      # Tracking DVC
├── img/                      # Illustrations
├── _minio/                   # Volume MinIO
├── .dvc/                     # Config DVC
├── docker-compose.yml        # MinIO
└── README.md                 # Documentation
```

## Commandes Principales

| Commande           | Fonction                        |
| ------------------ | ------------------------------- |
| dvc status         | État local des données          |
| dvc status --cloud | Synchronisation avec le remote  |
| dvc push           | Envoi des données vers MinIO    |
| dvc pull           | Récupération depuis MinIO       |
| dvc add <fichier>  | Ajout d’un fichier au suivi DVC |
| git add <.dvc>     | Ajout des métadonnées DVC à Git |

## Concepts Clés

- **DVC** : Gestion du versionnement des données, séparation des métadonnées (Git) et des blobs (MinIO)
- **MinIO** : Stockage S3 compatible, interface web pour la gestion des artefacts

## Vérification

- MinIO opérationnel sur http://localhost:9001
- DVC initialisé et remote configuré
- Données trackées et synchronisées

## Ressources

- [Documentation DVC](https://dvc.org/doc)
- [Documentation MinIO](https://min.io/docs/)
- [Dataset Iris](https://archive.ics.uci.edu/ml/datasets/iris)

## Auteur

Projet réalisé dans le cadre du cours MLOps.

# mlops-dvc-iris

Pipeline MLOps pour iris avec DVC.

- Gestion des données et des images
- Orchestration via Docker Compose

## Accès

Ouvrir le dossier `mlops-dvc-iris`.

## Démarrage rapide

Voir le fichier `README.md` du dossier pour les instructions détaillées.
