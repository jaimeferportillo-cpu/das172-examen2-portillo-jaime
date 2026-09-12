"""Pruebas unitarias de AeroCargo-Matrix (ejecutar: python -m unittest -v)."""

import unittest

from aerocargo import (
    calcular_ocupacion,
    evaluar_balance,
    extraer_submatriz_critica,
    validar_matrices,
)


class PruebasAeroCargo(unittest.TestCase):
    def test_validacion_correcta_y_matriz_minima(self):
        self.assertTrue(validar_matrices([[0, 2], [3, 4]], [[1, 2], [3, 4]]))

    def test_rechaza_dimensiones_irregulares_o_distintas(self):
        self.assertFalse(validar_matrices([[1, 2], [3]], [[2, 2], [2, 2]]))
        self.assertFalse(validar_matrices([[1, 2], [3, 4]], [[2, 2]]))

    def test_rechaza_pesos_negativos_y_capacidad_cero(self):
        self.assertFalse(validar_matrices([[1, -1], [3, 4]], [[2, 2], [2, 2]]))
        self.assertFalse(validar_matrices([[1, 1], [3, 4]], [[2, 0], [2, 2]]))

    def test_ocupacion_y_sobrecarga_estricta(self):
        porcentajes, posiciones = calcular_ocupacion(
            [[0, 100], [120, 50]], [[100, 100], [100, 100]]
        )
        self.assertEqual(porcentajes, [[0.0, 100.0], [120.0, 50.0]])
        self.assertEqual(posiciones, [(1, 0)])

    def test_balance_columnas_pares(self):
        totales, desbalance, aprobado = evaluar_balance([[10, 20], [30, 40]], 20)
        self.assertEqual(totales, [30, 70])
        self.assertEqual(desbalance, 20)
        self.assertTrue(aprobado)

    def test_balance_columnas_impares_omite_centro(self):
        totales, desbalance, aprobado = evaluar_balance([[10, 999, 20], [30, 999, 40]], 20)
        self.assertEqual(totales, [1029, 1069])
        self.assertEqual(desbalance, 20)
        self.assertTrue(aprobado)

    def test_submatriz_por_promedio(self):
        matriz = [[10, 20, 30], [40, 200, 210], [50, 220, 230]]
        self.assertEqual(
            extraer_submatriz_critica(matriz, 2, 2), [[200, 210], [220, 230]]
        )

    def test_submatriz_por_cantidad_de_sobrecargas(self):
        matriz = [[150, 150, 10], [150, 10, 200], [10, 200, 200]]
        self.assertEqual(
            extraer_submatriz_critica(matriz, 2, 2, "sobrecargas"),
            [[10, 200], [200, 200]],
        )

    def test_entradas_no_se_modifican(self):
        cargas = [[1, 2], [3, 4]]
        capacidades = [[2, 2], [4, 4]]
        copia_cargas = [fila[:] for fila in cargas]
        copia_capacidades = [fila[:] for fila in capacidades]
        porcentajes, _ = calcular_ocupacion(cargas, capacidades)
        extraer_submatriz_critica(porcentajes, 1, 1)
        self.assertEqual(cargas, copia_cargas)
        self.assertEqual(capacidades, copia_capacidades)

    def test_errores_de_ventana_y_tolerancia(self):
        with self.assertRaises(ValueError):
            extraer_submatriz_critica([[10, 20], [30, 40]], 3, 1)
        with self.assertRaises(ValueError):
            evaluar_balance([[1, 2], [3, 4]], -1)

    def test_balance_rechazado(self):
        totales, desbalance, aprobado = evaluar_balance(
            [[100, 10], [100, 10]], 50
        )
        self.assertEqual(totales, [110, 110])
        self.assertEqual(desbalance, 180)
        self.assertFalse(aprobado)
if __name__ == "__main__":
    unittest.main()
