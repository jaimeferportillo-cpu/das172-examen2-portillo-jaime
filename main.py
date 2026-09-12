"""Demostración completa del sistema AeroCargo-Matrix."""

from aerocargo import (
    calcular_ocupacion,
    evaluar_balance,
    extraer_submatriz_critica,
    validar_matrices,
)


def imprimir_matriz(titulo, matriz, formato="{:8.2f}"):
    print(f"\n{titulo}")
    for fila in matriz:
        print(" ".join(formato.format(valor) for valor in fila))


def main():
    cargas = [
        [700, 650, 600, 550],
        [800, 950, 700, 500],
        [500, 600, 900, 850],
        [400, 450, 500, 600],
    ]
    capacidades = [
        [800, 700, 700, 650],
        [750, 900, 800, 700],
        [600, 650, 850, 800],
        [500, 500, 550, 650],
    ]
    tolerancia = 300

    print("AEROCARGO-MATRIX - AUDITORÍA DE CARGA")
    if not validar_matrices(cargas, capacidades):
        print("Datos rechazados: revise dimensiones y valores.")
        return

    porcentajes, sobrecargas = calcular_ocupacion(cargas, capacidades)
    totales_fila, desbalance, aprobado = evaluar_balance(cargas, tolerancia)
    critica = extraer_submatriz_critica(porcentajes, 2, 2, "promedio")

    imprimir_matriz("Cargas reales (kg):", cargas, "{:8.0f}")
    imprimir_matriz("Ocupación (%):", porcentajes)
    print(f"\nCeldas sobrecargadas (fila, columna): {sobrecargas}")
    print(f"Peso total por fila (kg): {totales_fila}")
    print(f"Desbalance lateral: {desbalance:.2f} kg")
    print(f"Tolerancia: {tolerancia:.2f} kg")
    print(f"Estado del balance: {'APROBADO' if aprobado else 'RECHAZADO'}")
    imprimir_matriz("Submatriz crítica 2 x 2 (%):", critica)


if __name__ == "__main__":
    main()
