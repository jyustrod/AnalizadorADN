"""Punto de entrada de la aplicación.

Este archivo permite arrancar el menú fácilmente con `python main.py`.
El bloque `if __name__ == "__main__"` asegura que solo se ejecute
cuando se lance directamente este archivo (y no al importarlo).
"""

from analizador_adn.app import main  # importar la función main que lanza el menú


if __name__ == "__main__":  # guard de módulo: ejecutar solo si es el script principal
    main()
