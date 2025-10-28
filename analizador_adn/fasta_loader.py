# Lector básico de archivos FASTA

class FastaLoader:
    # Guarda el nombre del archivo y las secuencias cargadas
    def __init__(self, filename=None):
        self.filename = filename
        # Guarda las secuencias como {encabezado: secuencia}
        self.sequences = {}

    def load_fasta(self, filename=None):
        # Carga el archivo FASTA y llena self.sequences
        # TODO: hacer la lectura real del archivo
        pass

    def get_sequences(self):
        # Devuelve las secuencias que se cargaron
        return self.sequences
