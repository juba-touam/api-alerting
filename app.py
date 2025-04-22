from flask import Flask, jsonify, request, render_template
from simulator import run_simulation, stop_simulation
import threading

app = Flask(__name__)

simulation_thread = None
simulation_status = {"running": False}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simulate", methods=["GET"])
def simulate():
    global simulation_thread, simulation_status

    count = int(request.args.get("count", 10))
    pause = float(request.args.get("pause", 0.0))

    stop_simulation.clear()
    simulation_status["running"] = True

    def run_and_update():
        run_simulation(count, pause)
        simulation_status["running"] = False

    simulation_thread = threading.Thread(target=run_and_update)
    simulation_thread.start()

    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    stop_simulation.set()
    simulation_status["running"] = False
    return jsonify({"status": "stopped"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"running": simulation_status["running"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
