# AnalizadorADN

Estructura base del proyecto para una aplicación de consola orientada a objetos que procesa secuencias de ADN en formato FASTA.

## Estructura del proyecto

- `analizador_adn/`
  - `__init__.py`
  - `app.py` — Controla el menú de la aplicación (pendiente de implementación)
  - `fasta_loader.py` — Carga de archivos FASTA (esqueleto)
  - `sequence_analyzer.py` — Análisis de contenido de nucleótidos (esqueleto)
  - `pattern_finder.py` — Búsqueda de patrones/motivos (esqueleto)
  - `translator.py` — Transcripción y traducción ADN→ARN→Proteína (esqueleto)
  - `mutator.py` — Simulación de mutaciones (esqueleto)
- `main.py` — Punto de entrada para ejecutar la app

## Requisitos técnicos

- Python 3.10+
- Ejecución prevista en consola mediante menú interactivo (por implementar)

## Próximos pasos

- Implementar la lógica de cada clase y el menú con opciones:
  1. Cargar archivo FASTA
  2. Análisis del contenido de nucleótidos
  3. Búsqueda de patrones y secuencias de interés
  4. Traducción del ADN a proteínas
  5. Simulación de mutaciones
  6. Salir

## Ejecución (una vez implementado)

```cmd
python -m venv .venv
.venv\Scripts\activate
python main.py
```
