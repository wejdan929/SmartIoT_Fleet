# 🚛 SmartIoT Fleet — Predictive Maintenance & Real-Time Monitoring

**SmartIoT Fleet** est une plateforme end-to-end de suivi télémétrique et de maintenance prédictive pour flottes de véhicules connectés. 

Le système simule l'acquisition de données capteurs à bord (vitesse, température, vibrations), orchestre la communication en temps réel via un bus MQTT, et intègre un modèle de Machine Learning pour la détection précoce des pannes logistiques.

---

## 🎯 Problématique & Solution

Dans le transport et la logistique, une panne non anticipée entraîne des coûts d'immobilisation élevés. **SmartIoT Fleet** répond à ce besoin en combinant :
- **Supervision temps réel (Event-Driven) :** Capture et filtrage continu des anomalies sur le réseau IoT.
- **Inférence par API REST :** Exposition du modèle prédictif pour l'interconnexion avec d'autres systèmes décisionnels.
- **Visualisation dynamique :** Suivi des indicateurs clés via un tableau de bord interactif.

---

## 🏗️ Architecture Technique

```text
[ Capteurs Véhicule ] ──(MQTT / Port 1883)──> [ Broker Pub/Sub (HiveMQ) ]
                                                       │
                                 ┌─────────────────────┴─────────────────────┐
                                 ▼                                           ▼
                     [ alert_subscriber.py ]                        [ API FastAPI ]
                     (Filtrage & Alertes Temps Réel)              (Endpoint /predict)
                                                                             │
                                                                             ▼
                                                                    [ Modèle Scikit-Learn ]