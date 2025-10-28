# Realizar análisis básicos sobre las secuencias de ADN

# Esta clase trabaja con un dict {encabezado: secuencia}
class SequenceAnalyzer:
    def __init__(self, sequences=None):
        # sequences puede venir None; con "or {}" se deja en dict vacío si no hay nada
        self.sequences = sequences or {}

    def set_sequences(self, sequences):
        # Actualizar el diccionario de secuencias cuando se cargue un FASTA
        self.sequences = sequences or {}

    def gc_content(self):
        # Calcular %GC por secuencia: (G + C) / total * 100
        resultados = {}
        for header, seq in self.sequences.items():  # .items() recorre clave y valor
            if not seq:
                resultados[header] = 0.0
                continue
            s = seq.upper()  # upper para evitar líos con minúsculas
            g = s.count("G")
            c = s.count("C")
            total = len(s)
            gc = ((g + c) / total * 100.0) if total > 0 else 0.0
            resultados[header] = round(gc, 2)  # redondear a 2 decimales
        return resultados

    def count_nucleotides(self):
        # Contar A, T, C, G y otros (por ejemplo, N)
        conteos = {}
        for header, seq in self.sequences.items():
            s = seq.upper()
            a = s.count("A")
            t = s.count("T")
            c = s.count("C")
            g = s.count("G")
            otros = len(s) - (a + t + c + g)
            conteos[header] = {"A": a, "T": t, "C": c, "G": g, "N": otros}
        return conteos

    def sequence_length(self):
        # Devolver la longitud (len) de cada secuencia
        largos = {}
        for header, seq in self.sequences.items():
            largos[header] = len(seq or "")  # por si viniera None
        return largos
