"""Persistencia local con reemplazo atómico y lectura del catálogo anterior."""
import json
import os
import pickle
import tempfile
from pathlib import Path

from arbol_nario import NodoNario
from arboles import ArbolLibros, NodoLibro
from biblioteca import Biblioteca
from libro import Libro


def categoria_a_dict(nodo):
    return {"libros": nodo.libros, "hijos": {
        nombre: categoria_a_dict(hijo) for nombre, hijo in nodo.hijos.items()
    }}


def restaurar_categoria(nodo, datos):
    nodo.libros = datos["libros"]
    for nombre, contenido in datos["hijos"].items():
        hijo = NodoNario(nombre)
        restaurar_categoria(hijo, contenido)
        nodo.hijos[nombre] = hijo


class LectorCatalogo(pickle.Unpickler):
    def find_class(self, modulo, nombre):
        clases = {(c.__module__, c.__name__): c for c in (ArbolLibros, NodoLibro, Libro)}
        if (modulo, nombre) not in clases:
            raise pickle.UnpicklingError("Clase ajena al catálogo de libros")
        return clases[modulo, nombre]


def cargar_anterior(biblioteca):
    if Path("arbol_libros.pkl").exists():
        with open("arbol_libros.pkl", "rb") as archivo:
            biblioteca.arbol_libros = LectorCatalogo(archivo).load()
        pendientes = [biblioteca.arbol_libros.raiz]
        while pendientes:
            nodo = pendientes.pop()
            if nodo:
                biblioteca.libros.append(nodo.libro)
                pendientes.extend((nodo.derecha, nodo.izquierda))
    if Path("categorias.json").exists():
        with open("categorias.json", encoding="utf-8") as archivo:
            restaurar_categoria(biblioteca.arbol_categorias.raiz, json.load(archivo))


def cargar_biblioteca():
    biblioteca = Biblioteca()
    if not Path("biblioteca.json").exists():
        cargar_anterior(biblioteca)
        return biblioteca
    with open("biblioteca.json", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    for registro in datos["libros"]:
        libro = Libro(registro["titulo"], registro["autor"], registro["isbn"])
        libro.disponible = registro["disponible"]
        biblioteca.libros.append(libro)
        biblioteca.arbol_libros.insertar(libro.isbn, libro)
    for registro in datos["usuarios"]:
        biblioteca.registrar_usuario(registro["id"], registro["nombre"])
        biblioteca.usuarios[registro["id"]].libros_prestados = registro["libros_prestados"]
    restaurar_categoria(biblioteca.arbol_categorias.raiz, datos["categorias"])
    return biblioteca


def guardar_datos(biblioteca):
    datos = {"libros": [vars(libro) for libro in biblioteca.libros],
             "usuarios": [vars(usuario) for usuario in biblioteca.usuarios.values()],
             "categorias": categoria_a_dict(biblioteca.arbol_categorias.raiz)}
    with tempfile.NamedTemporaryFile(dir=".", prefix=".biblioteca-", suffix=".tmp",
                                     mode="w", encoding="utf-8", delete=False) as archivo:
        temporal = Path(archivo.name)
        try:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
        except BaseException:
            archivo.close()
            temporal.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporal, "biblioteca.json")
    finally:
        temporal.unlink(missing_ok=True)
