import requests
import time
from threading import Event

TARGET_URL = "https://int.scpi-invest.check-consulting.net/api/protected"
stop_simulation = Event()

def run_simulation(count, pause):
    for i in range(count):
        if stop_simulation.is_set():
            print(f"[{i}] Simulation arrêtée.")
            break

        try:
            headers = {"Authorization": "Bearer totally.invalid.token"}
            response = requests.get(TARGET_URL, headers=headers)
            if response.status_code == 401:
                print(f"[{i}] 401 reçu - échec d'authentification attendu")
            else:
                print(f"[{i}] Reçu {response.status_code} - pas un échec attendu")
        except Exception as e:
            print(f"[{i}] Erreur : {e}")

        time.sleep(pause)
