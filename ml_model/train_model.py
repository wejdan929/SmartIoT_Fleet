import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

CSV_FILE = "simulation/fleet_data.csv"
MODEL_FILE = "ml_model/model.pkl"

def main():
    print("--- Chargement des données IoT pour le Machine Learning ---")
    
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{CSV_FILE}' est introuvable.")
        return

    print(f"Nombre total de lignes chargées : {len(df)}")
    
    if "status" not in df.columns or df["status"].nunique() < 2:
        print("\nAttention : Il faut un peu plus de données variées (avec des NORMAL et des WARNING).")
        return

    X = df[["speed_kmh", "engine_temp_c", "vibration_level"]]
    y = df["status"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("\nEntraînement du modèle de Machine Learning en cours...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Entraînement terminé avec succès !")

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("\n--- Résultats de l'évaluation du modèle ---")
    print(f"Précision globale (Accuracy) : {accuracy * 100:.2f}%")
    print("\nRapport détaillé par catégorie :")
    print(classification_report(y_test, y_pred))

    # Sauvegarde du modèle entraîné
    os.makedirs("ml_model", exist_ok=True)
    joblib.dump(model, MODEL_FILE)
    print(f"\nModèle sauvegardé avec succès dans : {MODEL_FILE}")

if __name__ == "__main__":
    main()