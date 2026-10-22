import time
import random
import csv
import os
from datetime import datetime

# Liste des identifiants de véhicules de la flotte
VEHICLES = ["TRUCK-001", "BUS-042", "VAN-105", "TRUCK-012"]

# Chemin du fichier CSV de sortie
CSV_FILE = "simulation/fleet_data.csv"

def generate_sensor_data(vehicle_id):
    """Simule la génération de données IoT pour un véhicule donné."""
    temperature = round(random.uniform(70.0, 115.0), 2)  # Température moteur en °C
    vibration = round(random.uniform(0.5, 4.5), 2)      # Niveau de vibration en mm/s
    speed = round(random.uniform(0.0, 90.0), 1)          # Vitesse en km/h
    
    status = "NORMAL"
    if temperature > 105.0 or vibration > 3.8:
        status = "WARNING"

    data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "vehicle_id": vehicle_id,
        "speed_kmh": speed,
        "engine_temp_c": temperature,
        "vibration_level": vibration,
        "status": status
    }
    return data

def main():
    print("--- Démarrage de la simulation IoT avec enregistrement CSV ---")
    print(f"Les données seront sauvegardées dans : {CSV_FILE}")
    print("Appuie sur Ctrl + C pour arrêter la simulation.\n")
    
    # Vérifier si le fichier existe déjà pour savoir s'il faut écrire l'en-tête
    file_exists = os.path.exists(CSV_FILE)
    
    # Ouvrir le fichier CSV en mode écriture/ajout (append)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        fieldnames = ["timestamp", "vehicle_id", "speed_kmh", "engine_temp_c", "vibration_level", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Si le fichier est nouveau, on écrit la ligne d'en-tête du tableau
        if not file_exists:
            writer.writeheader()
        
        try:
            while True:
                vehicle = random.choice(VEHICLES)
                sensor_packet = generate_sensor_data(vehicle)
                
                # Écrire la ligne dans le fichier CSV
                writer.writerow(sensor_packet)
                f.flush()  # Force l'écriture immédiate sur le disque
                
                # Afficher la ligne dans le terminal
                print(f"Enregistré -> {sensor_packet}")
                
                # Pause de 2 secondes
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n--- Simulation arrêtée. Fichiers de données sauvegardés avec succès ! ---")

if __name__ == "__main__":
    main()