from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Mengaktifkan CORS agar bisa diakses dari frontend

def get_localhost_ports():
    try:
        result = subprocess.run("lsof -i -P -n | grep LISTEN", shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return []
        
        lines = result.stdout.strip().split("\n")
        ports = []

        for line in lines:
            parts = line.split()
            if len(parts) >= 9 and ("127.0.0.1" in parts[-2] or "localhost" in parts[-2]):
                ports.append({
                    "process": parts[0],
                    "pid": parts[1],
                    "user": parts[2],
                    "port": parts[-2].split(":")[-1]
                })

        return ports
    except Exception as e:
        return {"error": str(e)}

@app.route("/api/localhost_ports")
def localhost_ports():
    return jsonify(get_localhost_ports())

@app.route("/api/kill_process/<pid>", methods=["POST"])
def kill_process(pid):
    try:
        # Gunakan perintah kill -9 <pid>
        os.system(f"kill -9 {pid}")
        return jsonify({"status": "success", "message": f"Process {pid} terminated"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
