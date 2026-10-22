import streamlit as st
import pandas as pd
import joblib
import os

# Configuration de la page Streamlit
st.set_page_config(
    page_title="SmartIoT Fleet - Monitoring",
    page_icon="🚚",
    layout="wide"
)

CSV_FILE = "simulation/fleet_data.csv"
MODEL_FILE = "ml_model/model.pkl"

st.title("🚚 SmartIoT Fleet - Tableau de Bord de Maintenance Prédictive")
st.markdown("Surveillance en temps réel des véhicules et prédictions IoT.")

# 1. Chargement du modèle Machine Learning
@st.cache_resource
def load_ml_model():
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    return None

model = load_ml_model()

# 2. Vérification et chargement des données CSV
if not os.path.exists(CSV_FILE):
    st.error(f"Le fichier de données '{CSV_FILE}' n'existe pas encore. Lance d'abord le simulateur !")
else:
    df = pd.read_csv(CSV_FILE)
    
    st.button("🔄 Rafraîchir les données")

    # Section 1 : Métriques globales
    st.subheader("📊 Vue d'ensemble de la Flotte")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Relevés IoT", len(df))
    col2.metric("Véhicules Actifs", df["vehicle_id"].nunique())
    col3.metric("Alertes (WARNING)", len(df[df["status"] == "WARNING"]))
    col4.metric("États Normaux", len(df[df["status"] == "NORMAL"]))

    st.divider()

    # Section 2 : Tableau des derniers relevés
    st.subheader("📡 Derniers Relevés des Capteurs & Prédictions ML")
    recent_df = df.tail(10).sort_index(ascending=False).copy()
    
    if model is not None:
        X_recent = recent_df[["speed_kmh", "engine_temp_c", "vibration_level"]]
        recent_df["Prediction_IA"] = model.predict(X_recent)
    
    st.dataframe(recent_df, use_container_width=True)

    st.divider()

    # Section 3 : Graphiques natifs de base de Streamlit (sans design forcé)
    st.subheader("📈 Évolution des Capteurs")
    col_graph1, col_graph2 = st.columns(2)

    with col_graph1:
        st.write("Température Moteur (°C)")
        st.line_chart(df.set_index("timestamp")["engine_temp_c"])

    with col_graph2:
        st.write("Niveau de Vibration (mm/s)")
        st.line_chart(df.set_index("timestamp")["vibration_level"])