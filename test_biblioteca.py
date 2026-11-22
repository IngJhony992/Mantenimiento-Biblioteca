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

    def test_hu02_buscar_titulo_y_autor(self):
        self.b.registrar_libro("El río", "Elena Ríos", "102")
        self.assertEqual([l.isbn for l in self.b.buscar_texto("ríos")], ["101", "102"])
        self.assertEqual([l.isbn for l in self.b.buscar_texto("LUNA")], ["101"])
        self.assertEqual(self.b.buscar_texto("ausente"), [])

    def test_hu03_rechazar_isbn_repetido(self):
        with self.assertRaises(ValueError):
            self.b.registrar_libro("Otro título", "Otro autor", " 101 ")
        self.assertEqual(len(self.b.libros), 1)
        self.assertEqual(self.b.buscar_libro("101").titulo, "Luna azul")

    def test_hu04_validar_titular(self):
        self.b.registrar_usuario("02", "Luis")
        self.b.prestar_libro("101", "01", "2026-11-21")
        self.assertFalse(self.b.devolver_libro("101", "02"))
        self.assertFalse(self.b.buscar_libro("101").disponible)
        self.assertEqual(self.b.usuarios["01"].libros_prestados, ["101"])
        with self.assertRaises(ValueError):
            self.b.registrar_usuario("01", "Luis")
        self.assertTrue(self.b.devolver_libro("101", "01"))
        self.assertTrue(self.b.buscar_libro("101").disponible)
