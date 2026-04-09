from flask import Flask, jsonify, request, send_from_directory
import os
from lista_doble import HospitalDoubleList, Patient

app = Flask(__name__, static_folder="static")
hospital = HospitalDoubleList()

_demo = [
    ("Maria Lopez",    "10010001", "medicine",    42),
    ("Jorge Ramirez",  "10010002", "cardiology",  67),
    ("Valentina Cruz", "10010003", "pediatrics",  6),
]

for name, id_num, spec, age in _demo:
    hospital.add_to_back(Patient(name, id_num, spec, age))

@app.route("/api/patients", methods=["GET"])
def get_patients():
    return jsonify({"patients": hospital.traverse_forward(), "total": len(hospital)})

@app.route("/api/patients", methods=["POST"])
def add_patient():
    data = request.json
    name = data.get("name", "").strip()
    id_number = data.get("id_number", "").strip()
    specialty = data.get("specialty", "medicine").strip()
    age = int(data.get("age", 0))
    urgent = data.get("urgent", False)

    if not name or not id_number:
        return jsonify({"error": "Name and ID are required"}), 400

    if hospital.find_by_id(id_number):
        return jsonify({"error": "Patient ID already exists"}), 409

    patient = Patient(name, id_number, specialty, age)
    if urgent or specialty.lower() == "emergency":
        hospital.add_to_front(patient)
    else:
        hospital.add_to_back(patient)

    return jsonify({"message": "Patient added", "patient": patient.to_dict()}), 201

@app.route("/api/serve", methods=["DELETE"])
def serve_patient():
    patient = hospital.serve_next()
    if patient is None:
        return jsonify({"error": "No patients in queue"}), 404
    return jsonify({"message": "Patient served", "patient": patient.to_dict()})

@app.route("/api/patients/<id_number>", methods=["DELETE"])
def delete_patient(id_number):
    patient = hospital.remove_by_id(id_number)
    if patient is None:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify({"message": "Patient removed", "patient": patient.to_dict()})

@app.route("/api/stats", methods=["GET"])
def stats():
    patients = hospital.traverse_forward()
    counts = {}
    for p in patients:
        spec = p["specialty"]
        counts[spec] = counts.get(spec, 0) + 1
    return jsonify({"total": len(hospital), "by_specialty": counts})

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
