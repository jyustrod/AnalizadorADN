from __future__ import annotations

# Buscar patrones y motivos dentro de las secuencias

class PatternFinder:
    def __init__(self, sequences=None):
        self.sequences = sequences or {}

    def set_sequences(self, sequences):
        # Actualizar las secuencias desde el exterior
        self.sequences = sequences or {}

    def find_pattern(self, pattern):
        # Buscar un patrón de texto exacto (sin expresiones regulares)
        # Devolver {header: [posiciones]}
        if not pattern:
            return {}
        pattern_u = pattern.upper()
        hallazgos = {}
        for header, seq in self.sequences.items():
            s = seq.upper()
            posiciones = []
            start = 0
            # Buscar todas las ocurrencias del patrón
            while True:
                idx = s.find(pattern_u, start)
                if idx == -1:
                    break
                posiciones.append(idx)
                start = idx + 1
            hallazgos[header] = posiciones
        return hallazgos

    def find_repeats(self, min_length=2):
        # Identificar subcadenas repetidas con longitud mínima indicada
        # Nota: implementación simple con complejidad alta; adecuada para secuencias pequeñas
        if min_length is None or min_length < 1:
            min_length = 1
        resultados = {}
        for header, seq in self.sequences.items():
            s = seq.upper()
            vistos = {}
            repetidos = set()
            n = len(s)
            # Recorrer todas las subcadenas y marcar las que aparecen más de una vez
            for i in range(n):
                for j in range(i + min_length, n + 1):
                    sub = s[i:j]
                    if sub in vistos:
                        repetidos.add(sub)
                    else:
                        vistos[sub] = True
            # Ordenar por longitud descendente para priorizar las más largas
            resultados[header] = sorted(list(repetidos), key=lambda x: (-len(x), x))
        return resultados

    def find_motif(self, motif):
        # Determinar la frecuencia de un motivo (permitir solapamientos)
        # Devolver {header: cantidad}
        if not motif:
            return {}
        m = motif.upper()
        conteos = {}
        for header, seq in self.sequences.items():
            s = seq.upper()
            total = 0
            for i in range(0, max(0, len(s) - len(m) + 1)):
                if s[i:i+len(m)] == m:
                    total += 1
            conteos[header] = total
        return conteos
