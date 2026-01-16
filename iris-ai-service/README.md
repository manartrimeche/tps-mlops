# Iris AI Service

Application de classification Iris utilisant machine learning. Comprend une API FastAPI, une interface React et une orchestration Docker Compose pour un déploiement simple et reproductible.

## Architecture

```
iris-ai-service/
├── api/                       # Backend FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py           # Application principale
│       ├── models.py         # Schémas Pydantic
│       ├── db.py
│       └── model/
│           ├── model.joblib  # Modèle RandomForest entraîné
│           └── model_metadata.json
├── frontend/                  # Frontend React + Vite
│   ├── Dockerfile
│   ├── package.json
│   ├── nginx.conf
│   └── src/
├── docker-compose.yml         # Orchestration multi-services
└── monitoring/               # Configuration Prometheus/Grafana
```

## Démarrage Rapide

### Prérequis

- Docker Desktop (Windows/Mac) ou Docker Engine (Linux)
- Docker Compose v2.0+
- Ports 8000 et 5174 disponibles

### Installation et Lancement

```bash
# Cloner le projet
git clone <repository-url>
cd iris-ai-service

# Lancer l'application
docker compose up --build

# En arrière-plan
docker compose up --build -d
```

### Accéder à l'application

- **Interface utilisateur** : http://localhost:5174
- **API documentation (Swagger)** : http://localhost:8000/docs
- **Health check** : http://localhost:8000/health

## 🐳 Détails des Dockerfiles

### Configuration Docker

Les images sont construites avec des optimisations :

- **API** : Image Python 3.11 légère (~150 MB) avec FastAPI/Uvicorn
- **Frontend** : Multi-stage build (Node + Nginx) qui produit une image ~25 MB
- **Réseau** : Communication inter-conteneurs via réseau privé `iris-network`

## Commandes Docker Utiles

### Gestion des services

```bash
docker compose up -d              # Démarrer
docker compose down               # Arrêter
docker compose logs -f            # Voir les logs
docker compose logs -f api        # Logs du service api
docker compose ps                 # État des conteneurs
```

### Accès aux conteneurs

```bash
docker compose exec api bash      # Shell du conteneur API
docker compose exec frontend sh   # Shell du conteneur Frontend
```

### Reconstruction et nettoyage

```bash
docker compose build --no-cache   # Reconstruire sans cache
docker compose down -v            # Arrêter et supprimer les volumes
docker system prune -a --volumes  # Nettoyer tout
```

## API Endpoints

### Health Check

```http
GET /health
```

Vérifie que l'API et le modèle sont chargés correctement.

### Prédiction

```http
POST /predict
Content-Type: application/json

{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Retourne la classe prédite et les probabilités.

### Test avec PowerShell

```powershell
# Health check
Invoke-RestMethod -Uri http://localhost:8000/health

# Prédiction
$body = @{
  sepal_length = 5.1
  sepal_width = 3.5
  petal_length = 1.4
  petal_width = 0.2
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/predict `
  -Method Post -ContentType "application/json" -Body $body
```

## 🔒 Variables d'Environnement

| Variable        | Service  | Description              |
| --------------- | -------- | ------------------------ |
| `API_PORT`      | api      | Port d'écoute de l'API   |
| `CORS_ORIGINS`  | api      | Origines CORS autorisées |
| `VITE_API_BASE` | frontend | URL de base de l'API     |

Modifier dans `docker-compose.yml` pour les changer.

## Tests

```bash
# Tests unitaires dans le conteneur
docker compose exec api pytest tests/test_api.py

# Ou localement
cd api
pytest tests/test_api.py -v
```

## Dépannage

### Port déjà utilisé

```powershell
# Trouver le processus utilisant le port 8000
Get-NetTCPConnection -LocalPort 8000

# Tuer le processus
Stop-Process -Id <PID> -Force

# Ou modifier le port dans docker-compose.yml
```

### Erreur CORS - Frontend ne peut pas appeler l'API

Vérifier que `CORS_ORIGINS` dans `docker-compose.yml` correspond à l'URL du frontend.

### Erreur de build npm

```bash
docker compose build --no-cache
docker compose down --rmi all
docker compose up --build
```

### Conteneur qui s'arrête immédiatement

```bash
docker compose logs api  # Voir les erreurs
```

### Modèle non trouvé

```bash
ls api/app/model/      # Vérifier que model.joblib existe
docker compose build api
```

## Monitoring (Optionnel)

Prometheus et Grafana sont disponibles dans le dossier `monitoring/`. Pour les ajouter :

```bash
docker compose -f docker-compose.yml -f monitoring/docker-compose.monitoring.yml up
```

- Prometheus : http://localhost:9090
- Grafana : http://localhost:3000

## Ressources

- **FastAPI** : https://fastapi.tiangolo.com/
- **Docker** : https://docs.docker.com/
- **React + Vite** : https://vitejs.dev/
- **Nginx** : https://nginx.org/en/docs/
