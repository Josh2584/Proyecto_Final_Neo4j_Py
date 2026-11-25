"""Ejecutar con python app.py desde la carpeta del proyecto."""
import sys
from pathlib import Path

# Visual Studio puede usar un intérprete distinto al entorno del proyecto.
# El ZIP incluye el driver oficial y sus datos de zonas horarias.
sys.path.insert(0, str(Path(__file__).resolve().with_name("controlador_neo4j.zip")))

from app_desktop import main


if __name__ == "__main__":
    main()
