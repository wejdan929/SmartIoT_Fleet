import paho.mqtt.client as mqtt
import json

# Configuration du Broker MQTT public
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "smartiot/fleet/telemetry"

# Seuils critiques d'alerte
TEMP_THRESHOLD = 110.0  # en °C
VIBRATION_THRESHOLD = 3.5  # niveau de vibration

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Abonné avec succès au flux MQTT de la flotte !")
        client.subscribe(TOPIC)
    else:
        print(f"❌ Erreur de connexion au broker, code : {rc}")

def on_message(client, userdata, msg):
    try:
        # Récupération et décodage du message JSON reçu
        payload = json.loads(msg.payload.decode('utf-8'))
        
        vehicle_id = payload.get("vehicle_id")
        speed = payload.get("speed_kmh")
        temp = payload.get("engine_temp_c")
        vibration = payload.get("vibration_level")
        timestamp = payload.get("timestamp")
        
        # Vérification des conditions d'alerte
        alerts = []
        if temp > TEMP_THRESHOLD:
            alerts.append(f"🔥 SURCHAUFFE MOTEUR ({temp}°C > {TEMP_THRESHOLD}°C)")
        if vibration > VIBRATION_THRESHOLD:
            alerts.append(f"⚠️ VIBRATIONS ANORMALES ({vibration} > {VIBRATION_THRESHOLD})")
            
        # Affichage du statut dans le centre de supervision
        if alerts:
            print(f"\n🚨 [ALERTE CRITIQUE] - {timestamp} - Véhicule : {vehicle_id}")
            for alert in alerts:
                print(f"   -> {alert}")
            print(f"   (Vitesse : {speed} km/h)\n")
        else:
            print(f"🟢 [NORMAL] {timestamp} | {vehicle_id} -> Vitesse: {speed}km/h | Temp: {temp}°C | Vib: {vibration}")

    except Exception as e:
        print(f"⚠️ Erreur lors du traitement du message : {e}")

# Initialisation du client MQTT (syntaxe moderne paho-mqtt v2+)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print(f"Connexion au broker {BROKER} pour l'écoute des alertes...")
client.connect(BROKER, PORT, 60)

# Lancement de la boucle d'écoute en arrière-plan
client.loop_forever()