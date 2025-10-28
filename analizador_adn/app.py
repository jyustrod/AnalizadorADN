# Aplicación principal de consola
# Aquí se arma el menú y se conectan las clases

from .fasta_loader import FastaLoader
from .sequence_analyzer import SequenceAnalyzer
from .pattern_finder import PatternFinder
from .translator import Translator
from .mutator import Mutator


class DNAApp:
    # Clase que maneja la app en consola
    # Falta hacer el menú interactivo
    def __init__(self):
        # Creo las "herramientas" que voy a usar
        self.loader = FastaLoader()
        self.analyzer = SequenceAnalyzer()
        self.finder = PatternFinder()
        self.translator = Translator()
        self.mutator = Mutator()

    def run(self):
        # Aqui debería ir el menú con las opciones
        # TODO: implementar el menú paso a paso
        pass


def main():
    app = DNAApp()
    app.run()


if __name__ == "__main__":
    main()
