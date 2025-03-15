class ContenedorBebida:
    def __init__(self, capacidad: int, cantidad: int):
        self.capacidad = capacidad  # Capacidad en onzas
        self.cantidad = cantidad  # Número de vasos disponibles

    def tiene_vasos(self, cantidad_requerida: int) -> bool:
        return self.cantidad >= cantidad_requerida

    def dispensar_vaso(self):
        if self.cantidad > 0:
            self.cantidad -= 1
        else:
            raise ValueError("Error: No hay vasos disponibles")


class ModuloCafetera:
    def __init__(self, cantidad_cafe: int):
        self.cantidad_cafe = cantidad_cafe  # Cantidad total de café en onzas

    def tiene_cafe(self, cantidad_requerida: int) -> bool:
        return self.cantidad_cafe >= cantidad_requerida

    def dispensar_cafe(self, cantidad: int):
        if self.tiene_cafe(cantidad):
            self.cantidad_cafe -= cantidad
        else:
            raise ValueError("Error: No hay suficiente café disponible")


class ModuloAzucar:
    def __init__(self, cantidad_azucar: int):
        self.cantidad_azucar = cantidad_azucar  # Cantidad total de azúcar en cucharadas

    def tiene_azucar(self, cantidad_requerida: int) -> bool:
        return self.cantidad_azucar >= cantidad_requerida

    def dispensar_azucar(self, cantidad: int):
        if self.tiene_azucar(cantidad):
            self.cantidad_azucar -= cantidad
        else:
            raise ValueError("Error: No hay suficiente azúcar disponible")


class CafeteraAutomatizada:
    def __init__(self, cafe: int, azucar: int, vasos_pequenos: int, vasos_medianos: int, vasos_grandes: int):
        self.cafetera = ModuloCafetera(cafe)
        self.azucarero = ModuloAzucar(azucar)
        self.vasos = {
            "Pequeño": ContenedorBebida(3, vasos_pequenos),
            "Mediano": ContenedorBebida(5, vasos_medianos),
            "Grande": ContenedorBebida(7, vasos_grandes),
        }

    def preparar_cafe(self, tamaño: str, cucharadas_azucar: int = 0) -> str:
        if tamaño not in self.vasos:
            return "Error: Tamaño de vaso inválido"
        if not self.vasos[tamaño].tiene_vasos(1):
            return "Error: No hay vasos disponibles"
        if not self.cafetera.tiene_cafe(self.vasos[tamaño].capacidad):
            return "Error: No hay suficiente café"
        if not self.azucarero.tiene_azucar(cucharadas_azucar):
            return "Error: No hay suficiente azúcar"

        self.vasos[tamaño].dispensar_vaso()
        self.cafetera.dispensar_cafe(self.vasos[tamaño].capacidad)
        self.azucarero.dispensar_azucar(cucharadas_azucar)

        return f"Café servido: {tamaño} ({self.vasos[tamaño].capacidad} Oz) con {cucharadas_azucar} cucharadas de azúcar"


# Pruebas 
def test_preparacion_cafe():
    maquina = CafeteraAutomatizada(cafe=50, azucar=20, vasos_pequenos=5, vasos_medianos=5, vasos_grandes=5)
    assert maquina.preparar_cafe("Pequeño") == "Café servido: Pequeño (3 Oz) con 0 cucharadas de azúcar"
    assert maquina.preparar_cafe("Mediano", 2) == "Café servido: Mediano (5 Oz) con 2 cucharadas de azúcar"
    assert maquina.preparar_cafe("Grande", 1) == "Café servido: Grande (7 Oz) con 1 cucharadas de azúcar"


def test_errores_falta_insumos():
    maquina = CafeteraAutomatizada(cafe=10, azucar=10, vasos_pequenos=0, vasos_medianos=2, vasos_grandes=2)
    assert maquina.preparar_cafe("Pequeño") == "Error: No hay vasos disponibles"

    maquina = CafeteraAutomatizada(cafe=0, azucar=10, vasos_pequenos=5, vasos_medianos=5, vasos_grandes=5)
    assert maquina.preparar_cafe("Pequeño") == "Error: No hay suficiente café"

    maquina = CafeteraAutomatizada(cafe=10, azucar=0, vasos_pequenos=5, vasos_medianos=5, vasos_grandes=5)
    assert maquina.preparar_cafe("Pequeño", 1) == "Error: No hay suficiente azúcar"


def test_tamano_invalido():
    maquina = CafeteraAutomatizada(cafe=50, azucar=20, vasos_pequenos=5, vasos_medianos=5, vasos_grandes=5)
    assert maquina.preparar_cafe("ExtraGrande") == "Error: Tamaño de vaso inválido"