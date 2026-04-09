# 🏥 Hospital DoubleLink — Sistema de Turnos
### Estructuras de Datos · Lista Doblemente Enlazada (POO)
**Docente:** Jhonatan Andres Mideros Narvaez | **Semestre:** Cuarto

---

## 📌 Caso de Estudio

**Gestión de Turnos en un Hospital** usando una **Lista Doblemente Enlazada**.

Cada paciente es un **Nodo** con punteros `anterior` y `siguiente`.  
La lista permite:
- Insertar al final (paciente normal)
- Insertar al inicio (urgencias prioritarias)
- Eliminar el primero (atender siguiente)
- Eliminar por cédula (en cualquier posición)
- Recorrer en ambas direcciones (cabeza → cola / cola → cabeza)

---

## 🗂️ Estructura del Proyecto

```
hospital_turnos/
├── lista_doble.py      ← POO: Nodo, Paciente, ListaDobleHospital
├── app.py              ← Servidor Flask (API REST)
├── requirements.txt    ← Dependencias
├── static/
│   └── index.html      ← Frontend profesional
└── README.md
```

---

## ⚙️ Cómo ejecutar

### 1. Requisitos previos
- Python 3.10 o superior instalado
- Tener `pip` disponible

### 2. Instalar dependencias

Abre una terminal en la carpeta `hospital_turnos/` y ejecuta:

```bash
pip install -r requirements.txt
```

### 3. Iniciar el servidor

```bash
python app.py
```

Verás en la terminal:
```
=======================================================
  Hospital DoubleLink — Sistema de Turnos
  Abre tu navegador en: http://localhost:5000
=======================================================
```

### 4. Abrir el Frontend

Abre tu navegador y ve a:

```
http://localhost:5000
```

---

## 🧪 Probar solo la lista (sin frontend)

```bash
python lista_doble.py
```

---

## 🔗 Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | `/api/pacientes` | Obtener todos los pacientes en cola |
| POST   | `/api/pacientes` | Registrar nuevo paciente |
| DELETE | `/api/atender`   | Atender (eliminar) el primer paciente |
| DELETE | `/api/pacientes/<cedula>` | Eliminar paciente por cédula |
| GET    | `/api/buscar/<cedula>` | Buscar paciente sin eliminarlo |
| GET    | `/api/stats` | Estadísticas por especialidad |

---

## 📐 Diagrama de la Lista Doble

```
NULL ← [Cabeza: Urgencias] ↔ [Medicina] ↔ [Cardiología] → NULL
         ↑ primer nodo                        ↑ último nodo (cola)
```

Cada nodo almacena:
- `paciente` → datos del paciente
- `siguiente` → puntero al nodo siguiente
- `anterior`  → puntero al nodo anterior
