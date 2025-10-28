# Hace análisis básicos sobre las secuencias de ADN

class SequenceAnalyzer:
    def __init__(self, sequences=None):
        # Si no pasan secuencias, arranca con un diccionario vacío
        self.sequences = sequences or {}

    def gc_content(self):
        # Calcula el % de GC por secuencia
        # TODO: implementar cálculo real
        pass

    def count_nucleotides(self):
        # Cuenta A, T, C y G por cada secuencia
        # TODO: implementar conteo real
        pass

    def sequence_length(self):
        # Devuelve la longitud de cada secuencia
        # TODO: calcular longitudes
        pass
