# mlflow-cv-yolo

Expérimentation MLflow pour YOLOv8 sur COCO128.

- Suivi des runs avec MLflow
- Scripts d'entraînement
- DVC pour la gestion des données

## Accès

Ouvrir le dossier `mlflow-cv-yolo`.

## Démarrage rapide

Voir le fichier `README.md` du dossier pour les instructions détaillées.

# MLflow Experiment Tracking for Object Detection with YOLO

**MLOps Training Course - YOLO tiny Object Detection**

This project demonstrates best practices for experiment tracking using MLflow, comparing multiple model configurations, and making informed decisions about model promotion.

---

## 🎯 Learning Objectives

- Track and monitor multiple YOLO tiny model runs using MLflow
- Analyze and compare key metrics (mAP, precision, recall) across experiments
- Use MLflow UI to identify the best performing configuration
- Document and justify model promotion decisions
- Optionally register the selected model in MLflow's Model Registry (Staging/Production stages)

---

## ✅ Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.11+**
- **Git**
- **Docker Desktop** (for MLflow server and MinIO storage)
- **PowerShell** (Windows) or **bash** (Linux/macOS)

---

## � Getting Started

### Step 0: Fork and Clone the Repository

1. **Fork the repository** on GitHub/GitLab: [MLflow-CV-Yolo](https://github.com/your-fork/MLflow-CV-Yolo)
2. **Clone your fork** locally:

```bash
# Replace <YOUR_FORK_URL> with your fork's URL
git clone <YOUR_FORK_URL>
cd mlflow-cv-yolo
```

---

## 📖 Complete Setup Guide

### Step 1: Python Environment Setup

Choose the appropriate command for your operating system.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Linux/macOS (bash/zsh):**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Windows Command Prompt (CMD):**

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 2: Dataset Preparation with DVC Tracking

#### Create the Minimal Dataset

Generate a lightweight dataset (1 class: "person") from COCO128:

```bash
python tools/make_tiny_person_from_coco128.py
```

**Expected output:**

- **60 total images** (40 train, 10 val, 10 test)
- **1 class**: person
- **Location**: `data/tiny_coco/`

#### Track Dataset with DVC

Version your dataset using Data Version Control to ensure reproducibility:

```bash
# Initialize DVC (if not already done)
dvc init

# Track the entire dataset folder
dvc add data/tiny_coco -R

# Commit DVC metadata and configuration
git add data/tiny_coco.dvc .gitignore .dvc/ .gitattributes
git commit -m "Track dataset tiny_coco with DVC"
```

#### (Optional) Configure DVC Remote Storage

For local storage:

```bash
dvc remote add -d localfs ./dvcstore
dvc push
```

For MinIO (if configured in separate TP):

```bash
dvc remote add -d storage s3://mlops-dvc
dvc remote modify storage endpointurl http://localhost:9000
dvc remote modify storage use_ssl false
dvc remote modify storage region us-east-1
dvc push
```

---

### Step 3: Launch MLflow Backend Services

#### Start Docker Services

```bash
docker compose up -d
docker compose ps
docker compose logs -f mlflow  # Press Ctrl+C to exit
```

#### Verify Services

- **MLflow UI**: http://localhost:5000
- **MinIO Console**: http://localhost:9001 (credentials in `docker-compose.yml` or `mlflow.env`)

✅ **Checkpoint**: Open the MLflow interface in your browser to confirm it's running.

---

### Step 4: Configure MLflow Tracking URI

Set the environment variable so all training scripts use the same MLflow server.

**Linux/macOS:**

```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
```

**Windows PowerShell:**

```powershell
$env:MLFLOW_TRACKING_URI = "http://localhost:5000"
```

**Windows CMD:**

```cmd
set MLFLOW_TRACKING_URI=http://localhost:5000
```

---

### Step 5: Run a Baseline Experiment

Execute a single training run to verify everything is configured correctly.

**Using package module (recommended):**

```bash
python -m src.train_cv --epochs 3 --imgsz 320 --exp-name cv_yolo_tiny
```

**Or direct execution:**

```bash
python src/train_cv.py --epochs 3 --imgsz 320 --exp-name cv_yolo_tiny
```

**Estimated time**: 1-2 minutes

✅ **Checkpoint**: Verify that a new run appears in the MLflow UI at http://localhost:5000

---

### Step 6: Run Hyperparameter Grid Search

Generate 8 runs with different hyperparameter combinations to find the optimal configuration.

**Linux/macOS:**

```bash
chmod +x scripts/run_grid.sh
bash scripts/run_grid.sh
```

**Windows PowerShell:**

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_grid.ps1
```

**Windows CMD:**

```cmd
scripts\run_grid.cmd
```

**Estimated time**: 5-10 minutes

**Tested configurations:**

- **Image sizes**: 320, 416
- **Learning rates**: 0.005, 0.01
- **Random seeds**: 1, 42
- **Epochs**: 3 (fixed)

✅ **Checkpoint**: You should see 8-9 runs in the MLflow UI.

---

### Step 7: Compare Experiments in MLflow UI

#### Navigate to Your Experiment

1. Open http://localhost:5000
2. Go to **Experiments** menu → select `cv_yolo_tiny` or **All Experiments**
3. Filter to show **All runs**
4. Select multiple runs by checking the checkboxes
5. Click **Compare** button

#### Key Metrics to Analyze

When comparing runs, focus on these performance indicators:

| Metric        | Definition                                               |
| ------------- | -------------------------------------------------------- |
| **mAP@50**    | Average precision at 50% IoU threshold                   |
| **mAP@50-95** | Average precision across IoU thresholds (50%-95%)        |
| **Precision** | Ratio of correct detections among all predictions        |
| **Recall**    | Ratio of detected objects among all ground truth objects |

#### Artifacts Available for Each Run

Download and review these files from each run:

- `results.png` - Training curves (loss, mAP, precision, recall over epochs)
- `confusion_matrix.png` - Detection accuracy breakdown
- `PR_curve.png` - Precision-Recall curve
- `F1_curve.png` - F1-score curve across confidence thresholds
- `weights/best.pt` - Best model weights
- `weights/last.pt` - Final checkpoint weights

#### Training Curves Example

![Training curves](img/results.png)
_Figure 1: Training curves showing loss, mAP, precision, and recall progression_

**What to look for:**

- Box Loss should decrease consistently (indicates convergence)
- mAP@50 should increase progressively
- Precision and Recall should be well-balanced

#### Confusion Matrix Analysis

![Confusion matrix](img/confusion_matrix.png)
_Figure 2: Confusion matrix for "person" class detection_

**Understanding the matrix:**

- **True Positives (TP)**: People correctly detected ✓
- **False Positives (FP)**: Background incorrectly classified as person (minimize)
- **False Negatives (FN)**: People missed by the model (minimize)
- **True Negatives (TN)**: Background correctly ignored

---

### Step 8: Analyze Results and Promote Model

#### Export Experiment Results

In the MLflow comparison view:

- Click the **export as CSV** button (top right) to save metrics
- Take screenshots of the comparison table for documentation

#### Decision Documentation

Complete the decision template: `reports/templates/decision_template.md`

**Required sections:**

1. **Objectives & Constraints**
   - Primary goal (e.g., maximize mAP@50-95)
   - Limitations (small dataset, training time, hardware)

2. **Recommended Model**
   - Run ID of the best performer
   - Hyperparameters used (epochs, imgsz, lr, seed)
   - Achieved metrics (mAP, precision, recall)

3. **Comparative Analysis**
   - Compare 2-3 top-performing runs
   - Document pros and cons for each

4. **Risk Assessment**
   - Identify 4 key risks
   - Propose mitigation strategies

5. **Final Decision**
   - **Approve** ✅ or **Reject** ❌
   - Clear justification
   - Any conditions

6. **Next Steps**
   - Short-term actions
   - Medium-term improvements
   - Long-term considerations

---

## 📊 Example Results Comparison

| Run      | Epochs | ImgSz | LR    | Seed | mAP@50-95  | mAP@50 | Precision | Recall |
| -------- | ------ | ----- | ----- | ---- | ---------- | ------ | --------- | ------ |
| **Best** | 3      | 416   | 0.01  | 42   | **0.2729** | 0.3228 | 0.008     | 0.7742 |
| Alt 1    | 3      | 416   | 0.01  | 1    | 0.2586     | 0.3013 | 0.008     | 0.7742 |
| Alt 2    | 3      | 320   | 0.01  | 42   | 0.2314     | 0.2751 | 0.0084    | 0.7097 |
| Alt 3    | 3      | 320   | 0.005 | 42   | 0.2250     | 0.2680 | 0.0078    | 0.6935 |

**Key Insights:**

- Image size 416 outperforms 320 (+19% mAP@50-95)
- Learning rate 0.01 is superior to 0.005
- Seed 42 slightly better than seed 1 (variance < 6%)

**Optimal Configuration**: epochs=3, imgsz=416, lr=0.01, seed=42

---

## 🔗 Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [DVC Documentation](https://dvc.org/doc)
- [YOLOv8 Ultralytics Guide](https://docs.ultralytics.com/)
- [COCO Dataset](https://cocodataset.org/)

---

## 👤 Author

Dr. Salah Gontara - MLOps 2025-26

---

## 📜 License

This project is provided for educational purposes only.
