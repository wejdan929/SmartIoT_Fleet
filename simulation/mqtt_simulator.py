import paho.mqtt.client as mqtt
import json
import random
import time

# Configuration du Broker MQTT public
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "smartiot/fleet/telemetry"

# Callback de connexion
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connecté avec succès au Broker MQTT public !")
    else:
        print(f"❌ Échec de la connexion, code d'erreur : {rc}")

# Initialisation du client MQTT (syntaxe moderne paho-mqtt v2+)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

print(f"Connexion au broker {BROKER}...")
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    print("🚀 Démarrage de la simulation IoT MQTT (Appuie sur Ctrl+C pour arrêter)...")
    while True:
        # Génération de données aléatoires pour un véhicule fictif
        vehicle_id = "TRUCK_001"
        speed = round(random.uniform(40.0, 120.0), 2)
        engine_temp = round(random.uniform(75.0, 115.0), 2)
        vibration = round(random.uniform(0.5, 4.5), 2)
        
        # Création du message au format JSON
        payload = {
            "vehicle_id": vehicle_id,
            "speed_kmh": speed,
            "engine_temp_c": engine_temp,
            "vibration_level": vibration,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Publication du message sur le topic MQTT
        client.publish(TOPIC, json.dumps(payload))
        print(f"📡 Données publiées sur [{TOPIC}] -> {payload}")
        
        # Pause de 3 secondes avant la prochaine mesure
        time.sleep(3)

except KeyboardInterrupt:
    print("\n🛑 Arrêt du simulateur MQTT.")
    client.loop_stop()
    client.disconnect()