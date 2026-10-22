# 🚚 SmartIoT Fleet - Maintenance Prédictive & Monitoring IoT

> Projet personnel de simulation IoT, d'entraînement de modèle de Machine Learning et de supervision de flotte en temps réel.

## 📋 À propos du projet
**SmartIoT Fleet** est une application complète de veille et de maintenance prédictive pour une flotte de véhicules connectés. Le système simule en continu des capteurs embarqués (température moteur, vibrations, vitesse), analyse les risques d'anomalies à l'aide d'un modèle d'intelligence artificielle supervisée, et restitue le tout sur un tableau de bord interactif.

## 🛠️ Architecture du Projet
```text
SmartIoT_Fleet/
│
├── simulation/
│   └── simulator.py     # Générateur de flux de données IoT en temps réel
├── ml_model/
│   └── train_model.py   # Script d'entraînement du modèle (Random Forest)
├── dashboard/
│   └── app.py           # Tableau de bord web interactif (Streamlit)
├── .gitignore
└── README.md