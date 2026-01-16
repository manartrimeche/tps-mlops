# TP6 : Optimisation des Hyperparamètres avec Optuna (YOLO tiny)

Ce projet correspond au TP6 du cours MLOps et a pour objectif d’industrialiser l’optimisation des hyperparamètres d’un modèle de vision par ordinateur (YOLOv8 tiny). Il s’appuie sur **Optuna** pour la recherche des meilleurs paramètres et **MLflow** pour le suivi des expériences.

---

## 🏗️ Architecture Technique

- **Modèle** : YOLOv8 tiny (ultralytics)
- **Jeu de données** : Tiny COCO (personnes uniquement), géré avec **DVC**
- **Suivi des expériences** : **MLflow** (paramètres, métriques, artefacts)
- **Stockage des artefacts** : **MinIO** (compatible AWS S3)
- **Optimisation** : **Optuna** (TPE)
- **Infrastructure** : Docker Compose

---

## 🚀 Installation et Démarrage

### 1. Prérequis

- Docker & Docker Compose
- Python 3.8 ou supérieur
- Git

### 2. Lancement des services

Démarrez la stack MLflow et MinIO :

```bash
docker compose up -d
```

- **MLflow UI** : http://localhost:5000
- **MinIO Console** : http://localhost:9001 (Utilisateur : `minio`, Mot de passe : `minio12345`)

### 3. Préparation de l’environnement Python

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Configuration des variables d’environnement

Pour permettre au script Python de communiquer avec MinIO et MLflow :

```powershell
$env:MLFLOW_TRACKING_URI = "http://localhost:5000"
$env:MLFLOW_S3_ENDPOINT_URL = "http://localhost:9000"
$env:AWS_ACCESS_KEY_ID = "minio"
$env:AWS_SECRET_ACCESS_KEY = "minio12345"
```

---

## 🏃‍♂️ Exécution des Expériences

### 1. Exécution du baseline

Lancez un entraînement simple pour valider la pipeline :

```bash
python -m src.train_cv --epochs 3 --imgsz 320 --exp-name yolo_baseline
```

### 2. Recherche par grille (Grid Search)

Lancez une recherche naïve sur une grille prédéfinie d’hyperparamètres :

```powershell
.\scripts\run_grid.ps1
```

### 3. Optimisation avancée avec Optuna

Lancez l’optimisation bayésienne des hyperparamètres :

```powershell
.\scripts\run_optuna.ps1 --n-trials 5
```

---

## 📊 Rapport de Décision

### 1. Contexte

- **Objectif** : Maximiser la précision de détection des personnes sur Tiny COCO
- **Modèle** : YOLOv8n (Nano), choisi pour sa rapidité
- **Métrique cible** : `metrics/mAP50(B)` (Mean Average Precision à IoU 0.5)

![Baseline Run](img/baseline-optuna.png)
_Fig 1. Run baseline initial dans MLflow_

### 2. Résumé des expériences Optuna

Une étude de 5 essais a permis d’optimiser deux hyperparamètres principaux : `epochs` (2 à 5) et `imgsz` (320 à 416).

| Trial ID    | Epochs | Imgsz   | mAP50 (Score) | Statut      |
| ----------- | ------ | ------- | ------------- | ----------- |
| Trial 0     | 2      | 320     | 0.150         | ✅          |
| Trial 1     | 3      | 320     | 0.146         | ✅          |
| Trial 2     | 4      | 320     | 0.155         | ✅          |
| Trial 3     | 3      | 416     | 0.151         | ✅          |
| **Trial 4** | **5**  | **320** | **0.168**     | **🏆 Best** |

### 3. Analyse et comparaison

#### Grid Search classique

![Grid Search Results](img/compare-without-optuna.png)
_Fig 2. Résultats des runs Grid Search classique. Les performances sont variables et la convergence n’est pas garantie._

#### Optuna vs Grid Search

- **Effet des epochs** : Augmenter le nombre d’epochs améliore nettement la performance (de 0.150 à 0.168). Le modèle continue de progresser à 5 epochs.
- **Effet de la taille d’image (imgsz)** : Passer de 320 à 416 n’apporte pas de gain significatif pour peu d’epochs, mais augmente le temps de calcul.
- **Optuna vs Grid Search** : Optuna converge rapidement vers les meilleurs paramètres sans tester toutes les combinaisons inefficaces.

![Comparison With Optuna](img/compare-with_optuna.png)
_Fig 3. Comparaison incluant les runs Optuna, illustrant l’exploration efficace des hyperparamètres._

### 4. Recommandation pour le staging

Nous recommandons d’utiliser les hyperparamètres du **Trial 4** pour l’environnement de staging :

- **Configuration retenue** :
  - `epochs`: **5** (ou plus si le temps le permet)
  - `imgsz`: **320** (plus rapide que 416)
- **Performance attendue** : mAP50 ≈ **0.168**

### 5. Discussion : Apport d’Optuna en MLOps

L’intégration d’Optuna dans la pipeline MLOps offre plusieurs avantages :

1. **Efficacité** : Optuna (TPE) cible les zones prometteuses, économisant du temps et des ressources GPU.
2. **Automatisation** : L’optimisation est automatisée, permettant de lancer des études sans supervision continue.
3. **Tracking unifié** : Grâce à MLflow, chaque essai est tracé et reproductible, assurant la traçabilité du cycle de vie du modèle.

---

# optuna-cv-yolo

Optimisation d'hyperparamètres YOLOv8 avec Optuna.

- DVC pour la gestion des données
- MLflow pour le suivi des runs
- Scripts d'entraînement et pipelines ZenML

## Accès

Ouvrir le dossier `optuna-cv-yolo`.

## Démarrage rapide

Voir le fichier `README.md` du dossier pour les instructions détaillées.
