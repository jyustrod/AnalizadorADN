import random
from .translator import Translator

# Simular mutaciones sobre una secuencia de ADN
class Mutator:
    def __init__(self):
        # Reutilizar el traductor para comparar el efecto en proteínas
        self.translator = Translator()
        # Definir bases válidas para ADN
        self.valid_bases = {"A", "T", "C", "G"}

    def point_mutation(self, seq, position, new_base):
        # Realizar una mutación puntual en una posición específica (0-index)
        if seq is None:
            raise ValueError("La secuencia no puede ser None")
        if position < 0 or position >= len(seq):
            raise ValueError("La posición está fuera del rango de la secuencia")
        nb = (new_base or "").upper()
        if nb not in self.valid_bases:
            raise ValueError("La nueva base debe ser A, T, C o G")
        # Construir la secuencia mutada de manera simple
        listado = list(seq.upper())
        listado[position] = nb
        return "".join(listado)

    def random_mutations(self, seq, num_mutations):
        # Aplicar varias mutaciones aleatorias en posiciones distintas cuando sea posible
        if not seq:
            return seq
        n = len(seq)
        if num_mutations <= 0:
            return seq
        num_mut = min(num_mutations, n)
        pos = random.sample(range(n), k=num_mut)
        bases = ["A", "T", "C", "G"]
        nuevo = list(seq.upper())
        for p in pos:
            actual = nuevo[p]
            # Elegir una base diferente a la actual
            opciones = [b for b in bases if b != actual]
            nuevo[p] = random.choice(opciones)
        return "".join(nuevo)

    def compare_proteins(self, original_seq, mutated_seq):
        # Comparar las proteínas traducidas de la secuencia original y la mutada
        # Devolver un dict con ambas proteínas y un indicador de igualdad
        rna_o = self.translator.transcribe_dna_to_rna(original_seq)
        rna_m = self.translator.transcribe_dna_to_rna(mutated_seq)
        prot_o = self.translator.translate_to_protein(rna_o)
        prot_m = self.translator.translate_to_protein(rna_m)
        iguales = (prot_o == prot_m)
        return {
            "original": prot_o,
            "mutado": prot_m,
            "iguales": iguales,
        }
