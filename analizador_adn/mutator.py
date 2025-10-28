import random

# Este bloque try/except sirve para que el import funcione tanto si se ejecuta como paquete
# (import relativo) como si se lanza el archivo suelto (import absoluto). Así no casca el import.
try:
    from .translator import Translator
except Exception:
    from translator import Translator

# class define una "plantilla" de objetos. Aquí se crea un "Mutator" con métodos para mutar ADN.
class Mutator:
    def __init__(self):
        # __init__ es el "constructor": se ejecuta al crear la clase. "self" es la instancia en curso.
        # Se guarda un traductor para comparar el efecto de mutar a nivel de proteína.
        self.translator = Translator()
        # Un set (conjunto) guarda elementos únicos y permite comprobar pertenencia muy rápido (in).
        self.valid_bases = {"A", "T", "C", "G"}

    def point_mutation(self, seq, position, new_base):
        # def define una función/metodo. Aquí se hace una mutación puntual en índice 0-based.
        # if/raise: validar parámetros y avisar con excepciones si algo no cuadra.
        if seq is None:
            raise ValueError("La secuencia no puede ser None")
        if position < 0 or position >= len(seq):
            raise ValueError("La posición está fuera del rango de la secuencia")
        nb = (new_base or "").upper()
        if nb not in self.valid_bases:
            raise ValueError("La nueva base debe ser A, T, C o G")
        # Convertir a lista para poder cambiar un carácter (las str son inmutables). Luego unir con ''.join.
        listado = list(seq.upper())
        listado[position] = nb
        return "".join(listado)

    def random_mutations(self, seq, num_mutations):
        # Hacer varias mutaciones al azar. random.sample elige posiciones distintas sin repetir.
        if not seq:
            return seq
        n = len(seq)
        if num_mutations <= 0:
            return seq
        num_mut = min(num_mutations, n)
        pos = random.sample(range(n), k=num_mut)
        bases = ["A", "T", "C", "G"]  # lista simple; permite indexado y elección aleatoria
        nuevo = list(seq.upper())
        for p in pos:  # for recorre las posiciones seleccionadas
            actual = nuevo[p]
            # Crear una lista de opciones que excluya la base actual (comprensión de listas)
            opciones = [b for b in bases if b != actual]
            nuevo[p] = random.choice(opciones)  # elegir una base distinta al azar
        return "".join(nuevo)

    def compare_proteins(self, original_seq, mutated_seq):
        # Traducir ambas secuencias y comparar. Devolver un dict con resultados.
        rna_o = self.translator.transcribe_dna_to_rna(original_seq)
        rna_m = self.translator.transcribe_dna_to_rna(mutated_seq)
        prot_o = self.translator.translate_to_protein(rna_o)
        prot_m = self.translator.translate_to_protein(rna_m)
        iguales = (prot_o == prot_m)  # expresión booleana: True si son calcadas
        return {
            "original": prot_o,
            "mutado": prot_m,
            "iguales": iguales,
        }
