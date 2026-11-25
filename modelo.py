"""Conexión a la instancia de Neo4j Desktop y configuración del blog."""
import os
from pathlib import Path

from neo4j import GraphDatabase


CARPETA = Path(__file__).resolve().parent
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USUARIO = os.getenv("NEO4J_USERNAME", "neo4j")
BASE = os.getenv("NEO4J_DATABASE", "neo4j")

# Estas etiquetas también delimitan las operaciones de edición del servicio.
TIPOS = ("Usuario", "Categoria", "Etiqueta", "Articulo", "Comentario")


def conectar(uri, usuario, clave):
    """Comprueba la conexión antes de mostrar los formularios del blog."""
    driver = GraphDatabase.driver(uri, auth=(usuario, clave), connection_timeout=5,
                                  max_transaction_retry_time=5)
    try:
        driver.verify_connectivity()
    except Exception:
        driver.close()
        raise
    return driver
