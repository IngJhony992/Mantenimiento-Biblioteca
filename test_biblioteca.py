import os
import tempfile
import unittest
from biblioteca import Biblioteca
from persistencia import cargar_biblioteca, guardar_datos


class PruebasBiblioteca(unittest.TestCase):
    def setUp(self):
        self.b = Biblioteca()
        self.b.registrar_libro("Luna azul", "Elena Ríos", "101")
        self.b.registrar_usuario("01", "Ana")

    def test_hu01_recuperar_al_reabrir(self):
        self.b.agregar_libro_a_categoria("101", "Literatura")
        self.assertTrue(self.b.prestar_libro("101", "01", "2026-11-21"))
        with tempfile.TemporaryDirectory() as carpeta:
            anterior = os.getcwd()
            try:
                os.chdir(carpeta)
                guardar_datos(self.b)
                copia = cargar_biblioteca()
            finally:
                os.chdir(anterior)
        self.assertEqual(copia.usuarios["01"].libros_prestados, ["101"])
        self.assertFalse(copia.buscar_libro("101").disponible)
        self.assertEqual(copia.arbol_categorias.buscar_categoria("Literatura"), ["101"])
        self.assertTrue(copia.devolver_libro("101", "01"))
