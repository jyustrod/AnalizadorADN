from __future__ import annotations

# Buscar patrones y motivos dentro de las secuencias

class PatternFinder:
    def __init__(self, sequences=None):
        # Guardar el dict de secuencias; usar {} si viene None
        self.sequences = sequences or {}

    def set_sequences(self, sequences):
        # Actualizar desde fuera cuando cambie el conjunto de secuencias
        self.sequences = sequences or {}

    def find_pattern(self, pattern):
        # Buscar un patrón literal (sin expresiones regulares) y devolver posiciones donde aparece
        # Se usa str.find en bucle, moviendo el inicio de búsqueda para pillar todas las ocurrencias
        if not pattern:
            return {}
        p = pattern.upper()
        hallazgos = {}
        for header, seq in self.sequences.items():
            s = seq.upper()
            posiciones = []
            start = 0
            # while True: romper con break cuando no haya más hallazgos
            while True:
                idx = s.find(p, start)
                if idx == -1:
                    break
                posiciones.append(idx)
                start = idx + 1  # avanzar 1 para permitir solapamientos
            hallazgos[header] = posiciones
        return hallazgos

    def find_repeats(self, min_length=2):
        # Detectar subcadenas repetidas de longitud >= min_length
        # Esta versión recorre todas las subcadenas (coste alto, útil para aprender con secuencias cortas)
        if min_length is None or min_length < 1:
            min_length = 1
        resultados = {}
        for header, seq in self.sequences.items():
            s = seq.upper()
            vistos = {}
            repetidos = set()  # set para no duplicar resultados
            n = len(s)
            # Doble bucle para generar subcadenas s[i:j]
            for i in range(n):
                for j in range(i + min_length, n + 1):
                    sub = s[i:j]
                    if sub in vistos:
                        repetidos.add(sub)
                    else:
                        vistos[sub] = True
            resultados[header] = sorted(list(repetidos), key=lambda x: (-len(x), x))
        return resultados

    def find_motif(self, motif):
        # Contar cuántas veces aparece un motivo (permitiendo solapamientos)
        if not motif:
            return {}
        m = motif.upper()
        conteos = {}
        for header, seq in self.sequences.items():
            s = seq.upper()
            total = 0
            # Recorrer por ventanas del tamaño del motivo y comparar
            for i in range(0, max(0, len(s) - len(m) + 1)):
                if s[i:i+len(m)] == m:  # slicing (rebanado) de cadenas
                    total += 1
            conteos[header] = total
        return conteos
