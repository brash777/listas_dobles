"""
  Servidor Flask — Sistema de Turnos Hospitalarios
  Expone la lista doblemente enlazada como API REST
  y sirve el frontend.
"""

from flask import Flask, jsonify, request, send_from_directory
import os
from lista_doble import ListaDobleHospital, Paciente

app = Flask(__name__, static_folder="static")

# Instancia global de la lista doble
hospital = ListaDobleHospital()

# Datos de ejemplo al iniciar
_demo = [
    ("María López",    "10010001", "medicina",    42),
    ("Jorge Ramírez",  "10010002", "cardiologia",  67),
    ("Valentina Cruz", "10010003", "pediatria",     6),
    ("Ricardo Torres", "10010004", "odontologia",  30),
    ("Elena Morales",  "10010005", "medicina",     55),
]
for nombre, ced, esp, edad in _demo:
    hospital.agregar_al_final(Paciente(nombre, ced, esp, edad))

# ── Rutas API ────────────────────────────────────────────────

@app.route("/api/pacientes", methods=["GET"])
def get_pacientes():
    return jsonify({"pacientes": hospital.recorrer_adelante(), "total": len(hospital)})


@app.route("/api/pacientes", methods=["POST"])
def agregar_paciente():
    data = request.json
    nombre      = data.get("nombre", "").strip()
    cedula      = data.get("cedula", "").strip()
    especialidad = data.get("especialidad", "medicina").strip()
    edad        = int(data.get("edad", 0))
    urgente     = data.get("urgente", False)

    if not nombre or not cedula:
        return jsonify({"error": "Nombre y cédula son obligatorios"}), 400

    if hospital.buscar_por_cedula(cedula):
        return jsonify({"error": "Ya existe un paciente con esa cédula"}), 409

    paciente = Paciente(nombre, cedula, especialidad, edad)
    if urgente or especialidad.lower() == "urgencias":
        hospital.agregar_al_inicio(paciente)
    else:
        hospital.agregar_al_final(paciente)

    return jsonify({"mensaje": "Paciente agregado", "paciente": paciente.to_dict()}), 201


@app.route("/api/atender", methods=["DELETE"])
def atender_siguiente():
    paciente = hospital.atender_siguiente()
    if paciente is None:
        return jsonify({"error": "No hay pacientes en espera"}), 404
    return jsonify({"mensaje": "Paciente atendido", "paciente": paciente.to_dict()})


@app.route("/api/pacientes/<cedula>", methods=["DELETE"])
def eliminar_paciente(cedula):
    paciente = hospital.eliminar_por_cedula(cedula)
    if paciente is None:
        return jsonify({"error": "Paciente no encontrado"}), 404
    return jsonify({"mensaje": "Paciente eliminado", "paciente": paciente.to_dict()})


@app.route("/api/buscar/<cedula>", methods=["GET"])
def buscar_paciente(cedula):
    paciente = hospital.buscar_por_cedula(cedula)
    if paciente is None:
        return jsonify({"error": "Paciente no encontrado"}), 404
    return jsonify({"paciente": paciente.to_dict()})


@app.route("/api/stats", methods=["GET"])
def stats():
    pacientes = hospital.recorrer_adelante()
    conteo = {}
    for p in pacientes:
        esp = p["especialidad"]
        conteo[esp] = conteo.get(esp, 0) + 1
    return jsonify({"total": len(hospital), "por_especialidad": conteo})


# ── Servir frontend ──────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    print("=" * 55)
    print("  Hospital DoubleLink — Sistema de Turnos")
    print("  Abre tu navegador en: http://localhost:5000")
    print("=" * 55)
    app.run(debug=True, port=5000)
