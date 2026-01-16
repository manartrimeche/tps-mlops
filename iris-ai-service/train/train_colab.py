# You can paste this into Google Colab (or run locally) to train and export the model.
# Colab has scikit-learn preinstalled.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib, json, os

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)
print(classification_report(y_test, y_pred, target_names=iris.target_names))

os.makedirs("export", exist_ok=True)
joblib.dump(clf, "export/model.joblib")
meta = {
    "dataset": "sklearn.datasets.load_iris",
    "model": "RandomForestClassifier",
    "sklearn_version": joblib.__version__,
    "accuracy": acc,
    "target_names": list(map(str, iris.target_names)),
}
with open("export/model_metadata.json", "w") as f:
    json.dump(meta, f, indent=2)

print("Saved to ./export/model.joblib and ./export/model_metadata.json")
# Download from Colab: click Folder icon (left), right-click files in export/
# Place files in api/app/model/, then rebuild the API image.
