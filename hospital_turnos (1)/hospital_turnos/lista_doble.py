"""
=============================================================
  CASO DE ESTUDIO: Sistema de Gestión de Turnos Hospitalarios
  Estructura de Datos: Lista Doblemente Enlazada (POO)
  Docente: Jhonatan Andres Mideros Narvaez
  Semestre: Cuarto — Estructuras de Datos
=============================================================
"""


class Paciente:
    """Clase que representa la información de un paciente."""

    ESPECIALIDADES = {
        "urgencias":    {"color": "#EF4444", "icono": "🚨", "prioridad": 1},
        "cardiologia":  {"color": "#F97316", "icono": "❤️",  "prioridad": 2},
        "pediatria":    {"color": "#8B5CF6", "icono": "👶", "prioridad": 3},
        "medicina":     {"color": "#3B82F6", "icono": "🩺", "prioridad": 4},
        "odontologia":  {"color": "#10B981", "icono": "🦷", "prioridad": 5},
    }

    def __init__(self, nombre: str, cedula: str, especialidad: str, edad: int):
        self.nombre      = nombre
        self.cedula      = cedula
        self.especialidad = especialidad.lower()
        self.edad        = edad
        self.numero_turno: int | None = None

    def to_dict(self):
        info = self.ESPECIALIDADES.get(self.especialidad, {"color": "#6B7280", "icono": "🏥", "prioridad": 9})
        return {
            "nombre":      self.nombre,
            "cedula":      self.cedula,
            "especialidad": self.especialidad.capitalize(),
            "edad":        self.edad,
            "turno":       self.numero_turno,
            "color":       info["color"],
            "icono":       info["icono"],
        }

    def __str__(self):
        return (f"Turno #{self.numero_turno:03d} | {self.nombre} | "
                f"Cédula: {self.cedula} | {self.especialidad.capitalize()} | Edad: {self.edad}")


# ─────────────────────────────────────────────────────────────
#  NODO DE LA LISTA DOBLE
# ─────────────────────────────────────────────────────────────

class Nodo:
    """Nodo de la lista doblemente enlazada."""

    def __init__(self, paciente: Paciente):
        self.paciente:   Paciente    = paciente
        self.siguiente:  Nodo | None = None   # puntero al siguiente nodo
        self.anterior:   Nodo | None = None   # puntero al nodo anterior


# ─────────────────────────────────────────────────────────────
#  LISTA DOBLEMENTE ENLAZADA
# ─────────────────────────────────────────────────────────────

class ListaDobleHospital:
    """
    Lista doblemente enlazada que gestiona la cola de turnos
    del hospital.  Cada nodo almacena un Paciente y dos
    punteros (anterior / siguiente).
    """

    def __init__(self):
        self.cabeza:   Nodo | None = None   # primer nodo (cabeza)
        self.cola:     Nodo | None = None   # último nodo (cola)
        self.longitud: int         = 0
        self._contador_turno: int  = 1

    # ── Insertar ────────────────────────────────────────────

    def agregar_al_final(self, paciente: Paciente) -> Nodo:
        """Agrega un paciente al final de la lista (O(1))."""
        paciente.numero_turno = self._contador_turno
        self._contador_turno += 1

        nuevo = Nodo(paciente)

        if self.cabeza is None:          # lista vacía
            self.cabeza = nuevo
            self.cola   = nuevo
        else:
            nuevo.anterior  = self.cola  # enlace hacia atrás
            self.cola.siguiente = nuevo  # enlace hacia adelante
            self.cola       = nuevo

        self.longitud += 1
        return nuevo

    def agregar_al_inicio(self, paciente: Paciente) -> Nodo:
        """Agrega un paciente al inicio (urgencias prioritarias) (O(1))."""
        paciente.numero_turno = self._contador_turno
        self._contador_turno += 1

        nuevo = Nodo(paciente)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola   = nuevo
        else:
            nuevo.siguiente    = self.cabeza  # enlace hacia adelante
            self.cabeza.anterior = nuevo      # enlace hacia atrás
            self.cabeza        = nuevo

        self.longitud += 1
        return nuevo

    # ── Eliminar ────────────────────────────────────────────

    def atender_siguiente(self) -> Paciente | None:
        """Atiende (elimina) el primer paciente de la cola (O(1))."""
        if self.cabeza is None:
            return None

        paciente = self.cabeza.paciente

        if self.cabeza == self.cola:     # solo un nodo
            self.cabeza = None
            self.cola   = None
        else:
            self.cabeza          = self.cabeza.siguiente
            self.cabeza.anterior = None   # corta enlace hacia atrás

        self.longitud -= 1
        return paciente

    def eliminar_por_cedula(self, cedula: str) -> Paciente | None:
        """Elimina un paciente por su cédula en cualquier posición (O(n))."""
        actual = self.cabeza
        while actual:
            if actual.paciente.cedula == cedula:
                # --- nodo único ---
                if actual == self.cabeza and actual == self.cola:
                    self.cabeza = None
                    self.cola   = None
                # --- es la cabeza ---
                elif actual == self.cabeza:
                    self.cabeza          = actual.siguiente
                    self.cabeza.anterior = None
                # --- es la cola ---
                elif actual == self.cola:
                    self.cola          = actual.anterior
                    self.cola.siguiente = None
                # --- nodo intermedio ---
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior

                self.longitud -= 1
                return actual.paciente
            actual = actual.siguiente
        return None

    # ── Consultas ───────────────────────────────────────────

    def buscar_por_cedula(self, cedula: str) -> Paciente | None:
        """Busca un paciente sin eliminarlo (O(n))."""
        actual = self.cabeza
        while actual:
            if actual.paciente.cedula == cedula:
                return actual.paciente
            actual = actual.siguiente
        return None

    def recorrer_adelante(self) -> list[dict]:
        """Retorna la lista de pacientes de cabeza a cola."""
        resultado = []
        actual = self.cabeza
        while actual:
            resultado.append(actual.paciente.to_dict())
            actual = actual.siguiente
        return resultado

    def recorrer_atras(self) -> list[dict]:
        """Retorna la lista de pacientes de cola a cabeza."""
        resultado = []
        actual = self.cola
        while actual:
            resultado.append(actual.paciente.to_dict())
            actual = actual.anterior
        return resultado

    def esta_vacia(self) -> bool:
        return self.cabeza is None

    def __len__(self):
        return self.longitud

    def __str__(self):
        if self.esta_vacia():
            return "Lista vacía"
        nodos = []
        actual = self.cabeza
        while actual:
            nodos.append(str(actual.paciente))
            actual = actual.siguiente
        return "\n".join(nodos)


# ─────────────────────────────────────────────────────────────
#  PRUEBA RÁPIDA EN CONSOLA
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    hospital = ListaDobleHospital()

    hospital.agregar_al_final(Paciente("Ana García",    "1001", "medicina",    35))
    hospital.agregar_al_final(Paciente("Luis Pérez",    "1002", "cardiologia",  60))
    hospital.agregar_al_final(Paciente("Sofía Ruiz",    "1003", "pediatria",     8))
    hospital.agregar_al_inicio(Paciente("Carlos Mora",  "1004", "urgencias",    45))

    print("=== Turno actual (cabeza → cola) ===")
    print(hospital)

    print("\n=== Atendiendo siguiente paciente ===")
    atendido = hospital.atender_siguiente()
    print(f"Atendido: {atendido}")

    print("\n=== Lista restante ===")
    print(hospital)

    print("\n=== Búsqueda por cédula 1002 ===")
    encontrado = hospital.buscar_por_cedula("1002")
    print(encontrado)

    print("\n=== Eliminar paciente cédula 1003 ===")
    eliminado = hospital.eliminar_por_cedula("1003")
    print(f"Eliminado: {eliminado}")

    print("\n=== Lista final ===")
    print(hospital)
