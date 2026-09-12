"""Funciones puras para auditar la distribución de carga de una aeronave."""

from numbers import Real


def validar_matrices(cargas, capacidades):
    """Retorna True si ambas matrices son regulares, compatibles y válidas."""
    if not isinstance(cargas, (list, tuple)) or not isinstance(capacidades, (list, tuple)):
        return False
    if len(cargas) < 2 or len(cargas) != len(capacidades):
        return False
    if any(not isinstance(fila, (list, tuple)) for fila in (*cargas, *capacidades)):
        return False

    columnas = len(cargas[0])
    if columnas < 2:
        return False
    if any(len(fila) != columnas for fila in cargas):
        return False
    if any(len(fila) != columnas for fila in capacidades):
        return False

    def numero_valido(valor):
        return isinstance(valor, Real) and not isinstance(valor, bool)

    return all(numero_valido(v) and v >= 0 for fila in cargas for v in fila) and all(
        numero_valido(v) and v > 0 for fila in capacidades for v in fila
    )


def calcular_ocupacion(cargas, capacidades):
    """Calcula porcentajes y coordenadas con ocupación estrictamente mayor a 100 %."""
    if not validar_matrices(cargas, capacidades):
        raise ValueError("Las matrices de cargas y capacidades no son válidas.")

    porcentajes = [
        [(peso / capacidad) * 100.0 for peso, capacidad in zip(fila_c, fila_m)]
        for fila_c, fila_m in zip(cargas, capacidades)
    ]
    sobrecargas = [
        (i, j)
        for i, fila in enumerate(porcentajes)
        for j, porcentaje in enumerate(fila)
        if porcentaje > 100.0
    ]
    return porcentajes, sobrecargas


def evaluar_balance(cargas, tolerancia):
    """Retorna totales por fila, desbalance lateral y aprobación del balance."""
    if not isinstance(tolerancia, Real) or isinstance(tolerancia, bool) or tolerancia < 0:
        raise ValueError("La tolerancia debe ser un número mayor o igual a cero.")
    if not isinstance(cargas, (list, tuple)) or len(cargas) < 2:
        raise ValueError("La matriz de cargas debe tener al menos dos filas.")
    if any(not isinstance(f, (list, tuple)) for f in cargas):
        raise ValueError("Cada fila debe ser una lista o tupla.")
    columnas = len(cargas[0])
    if columnas < 2 or any(len(f) != columnas for f in cargas):
        raise ValueError("La matriz de cargas debe ser regular y de al menos 2 x 2.")
    if any(not isinstance(v, Real) or isinstance(v, bool) or v < 0 for f in cargas for v in f):
        raise ValueError("Los pesos deben ser números mayores o iguales a cero.")

    totales_fila = [sum(fila) for fila in cargas]
    mitad = columnas // 2
    izquierda = sum(sum(fila[:mitad]) for fila in cargas)
    inicio_derecha = mitad if columnas % 2 == 0 else mitad + 1
    derecha = sum(sum(fila[inicio_derecha:]) for fila in cargas)
    desbalance = abs(izquierda - derecha)
    return totales_fila, desbalance, desbalance <= tolerancia


def extraer_submatriz_critica(porcentajes, k, p, criterio="promedio"):
    """Extrae la ventana k x p más crítica y conserva sus valores.

    criterio='promedio': maximiza el promedio de ocupación.
    criterio='sobrecargas': maximiza la cantidad de celdas > 100 % y usa el
    promedio como desempate. En empates finales se conserva la primera ventana.
    """
    if not isinstance(porcentajes, (list, tuple)) or not porcentajes:
        raise ValueError("La matriz de porcentajes no puede estar vacía.")
    if any(not isinstance(f, (list, tuple)) for f in porcentajes):
        raise ValueError("Cada fila debe ser una lista o tupla.")
    columnas = len(porcentajes[0])
    if columnas == 0 or any(len(f) != columnas for f in porcentajes):
        raise ValueError("La matriz de porcentajes debe ser regular.")
    if any(not isinstance(v, Real) or isinstance(v, bool) for f in porcentajes for v in f):
        raise ValueError("Los porcentajes deben ser numéricos.")
    if not isinstance(k, int) or isinstance(k, bool) or not isinstance(p, int) or isinstance(p, bool):
        raise ValueError("Las dimensiones k y p deben ser enteras.")
    if not (1 <= k <= len(porcentajes) and 1 <= p <= columnas):
        raise ValueError("La ventana k x p no cabe dentro de la matriz.")
    if criterio not in {"promedio", "sobrecargas"}:
        raise ValueError("El criterio debe ser 'promedio' o 'sobrecargas'.")

    mejor_clave = None
    mejor = None
    for i in range(len(porcentajes) - k + 1):
        for j in range(columnas - p + 1):
            ventana = [list(fila[j : j + p]) for fila in porcentajes[i : i + k]]
            valores = [v for fila in ventana for v in fila]
            promedio = sum(valores) / len(valores)
            cantidad = sum(v > 100.0 for v in valores)
            clave = (promedio,) if criterio == "promedio" else (cantidad, promedio)
            if mejor_clave is None or clave > mejor_clave:
                mejor_clave = clave
                mejor = ventana
    return mejor
