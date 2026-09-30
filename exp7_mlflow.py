import pandas as pd
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# --------------------------------------------------
# 1. Load Wine Quality Dataset
# --------------------------------------------------

url = "https://raw.githubusercontent.com/duchesnay/pystatsml/master/datasets/iris.csv"

data = pd.read_csv(url)

print("Dataset shape:", data.shape)
print(data.head())

# --------------------------------------------------
# 2. Convert Wine Quality into Binary Classification
# --------------------------------------------------

# quality >= 7 -> Good Wine (1)
# quality < 7  -> Bad Wine (0)

data["quality"] = (data["quality"] >= 7).astype(int)

X = data.drop("quality", axis=1)
y = data["quality"]

# --------------------------------------------------
# 3. Train-Test Split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# --------------------------------------------------
# 4. Define Models
# --------------------------------------------------

models = {

    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    ),

    "XGBoost": XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss"
    )
}

# --------------------------------------------------
# 5. Create MLflow Experiment
# --------------------------------------------------

mlflow.set_experiment("Wine Quality Classification")

results = []

# --------------------------------------------------
# 6. Train and Log Each Model
# --------------------------------------------------

for model_name, model in models.items():

    with mlflow.start_run(run_name=model_name):

        print("\nTraining:", model_name)

        # Train
        model.fit(X_train, y_train)

        # Predictions
        y_pred = model.predict(X_test)

        # Probability for ROC-AUC
        y_prob = model.predict_proba(X_test)[:, 1]

        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)

        # Print metrics
        print("Accuracy :", accuracy)
        print("F1 Score :", f1)
        print("ROC-AUC  :", roc_auc)

        # --------------------------------------------------
        # Log Hyperparameters
        # --------------------------------------------------

        if model_name == "Logistic Regression":
            mlflow.log_param("model", "Logistic Regression")
            mlflow.log_param("max_iter", 1000)

        elif model_name == "Random Forest":
            mlflow.log_param("model", "Random Forest")
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("max_depth", 10)

        else:
            mlflow.log_param("model", "XGBoost")
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("max_depth", 5)
            mlflow.log_param("learning_rate", 0.1)

        # --------------------------------------------------
        # Log Metrics
        # --------------------------------------------------

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("roc_auc", roc_auc)

        # --------------------------------------------------
        # Confusion Matrix
        # --------------------------------------------------

        cm = confusion_matrix(y_test, y_pred)

        plt.figure(figsize=(5, 4))

        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["Bad", "Good"],
            yticklabels=["Bad", "Good"]
        )

        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.title(model_name + " - Confusion Matrix")

        plot_file = model_name.replace(" ", "_") + "_confusion_matrix.png"

        plt.savefig(plot_file)
        plt.close()

        # Log plot to MLflow
        mlflow.log_artifact(plot_file)

        # --------------------------------------------------
        # Log Model
        # --------------------------------------------------

        mlflow.sklearn.log_model(
            model,
            "model"
        )

        # Save results
        results.append({
            "model": model_name,
            "accuracy": accuracy,
            "f1_score": f1,
            "roc_auc": roc_auc
        })

# --------------------------------------------------
# 7. Display Results
# --------------------------------------------------

results_df = pd.DataFrame(results)

print("\n========== MODEL RESULTS ==========")
print(results_df)

# --------------------------------------------------
# 8. Select Best Model Programmatically
# --------------------------------------------------

best_model = results_df.sort_values(
    by="accuracy",
    ascending=False
).iloc[0]

print("\n========== BEST MODEL ==========")
print("Model   :", best_model["model"])
print("Accuracy:", best_model["accuracy"])
print("F1      :", best_model["f1_score"])
print("ROC-AUC :", best_model["roc_auc"])

# --------------------------------------------------
# 9. Select Best Run Using MLflow Client API
# --------------------------------------------------

from mlflow.tracking import MlflowClient

client = MlflowClient()

experiment = client.get_experiment_by_name(
    "Wine Quality Classification"
)

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.accuracy DESC"]
)

best_run = runs[0]

print("\n========== BEST MLflow RUN ==========")
print("Run ID:", best_run.info.run_id)
print("Accuracy:", best_run.data.metrics["accuracy"])
print("F1 Score:", best_run.data.metrics["f1_score"])
print("ROC-AUC:", best_run.data.metrics["roc_auc"])

print("\nBest model selected successfully.")