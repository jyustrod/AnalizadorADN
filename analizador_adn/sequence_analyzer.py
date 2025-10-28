# Realizar análisis básicos sobre las secuencias de ADN

class SequenceAnalyzer:
    def __init__(self, sequences=None):
        # Inicializar con un diccionario de secuencias o vacío
        self.sequences = sequences or {}

    def set_sequences(self, sequences):
        # Actualizar las secuencias después de la carga
        self.sequences = sequences or {}

    def gc_content(self):
        # Calcular el porcentaje de GC por secuencia
        # Devolver un dict {header: porcentaje}
        resultados = {}
        for header, seq in self.sequences.items():
            if not seq:
                resultados[header] = 0.0
                continue
            seq_upper = seq.upper()
            g = seq_upper.count("G")
            c = seq_upper.count("C")
            total = len(seq_upper)
            # Evitar división por cero por precaución
            gc = ((g + c) / total * 100.0) if total > 0 else 0.0
            resultados[header] = round(gc, 2)
        return resultados

    def count_nucleotides(self):
        # Contar A, T, C y G por cada secuencia
        # Devolver {header: {"A":n, "T":n, "C":n, "G":n, "N":n_otros}}
        conteos = {}
        for header, seq in self.sequences.items():
            s = seq.upper()
            a = s.count("A")
            t = s.count("T")
            c = s.count("C")
            g = s.count("G")
            # Contar caracteres no ATCG (por ejemplo, N)
            otros = len(s) - (a + t + c + g)
            conteos[header] = {"A": a, "T": t, "C": c, "G": g, "N": otros}
        return conteos

    def sequence_length(self):
        # Calcular la longitud de cada secuencia
        largos = {}
        for header, seq in self.sequences.items():
            largos[header] = len(seq or "")
        return largos
