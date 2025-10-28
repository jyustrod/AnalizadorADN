from __future__ import annotations


# Convertir ADN a ARN y luego a proteína
class Translator:
    def __init__(self):
        # Definir la tabla simple de codones -> aminoácidos (1 letra)
        self.codon_table = {
            # Fenilalanina
            "UUU": "F", "UUC": "F",
            # Leucina
            "UUA": "L", "UUG": "L", "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
            # Isoleucina
            "AUU": "I", "AUC": "I", "AUA": "I",
            # Metionina (inicio)
            "AUG": "M",
            # Valina
            "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
            # Serina
            "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S", "AGU": "S", "AGC": "S",
            # Prolina
            "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
            # Treonina
            "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
            # Alanina
            "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
            # Tirosina
            "UAU": "Y", "UAC": "Y",
            # Histidina
            "CAU": "H", "CAC": "H",
            # Glutamina
            "CAA": "Q", "CAG": "Q",
            # Asparagina
            "AAU": "N", "AAC": "N",
            # Lisina
            "AAA": "K", "AAG": "K",
            # Aspártico
            "GAU": "D", "GAC": "D",
            # Glutámico
            "GAA": "E", "GAG": "E",
            # Cisteína
            "UGU": "C", "UGC": "C",
            # Triptófano
            "UGG": "W",
            # Arginina
            "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
            # Glicina
            "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G",
            # STOP
            "UAA": "*", "UAG": "*", "UGA": "*",
        }

    def transcribe_dna_to_rna(self, dna_seq):
        # Reemplazar T por U para convertir de ADN a ARN
        if dna_seq is None:
            return ""
        return (dna_seq.upper().replace("T", "U").replace("\n", "").replace(" ", ""))

    def translate_to_protein(self, rna_seq):
        # Traducir ARN a aminoácidos utilizando la tabla de codones
        # Interrumpir en codón de paro (*)
        if not rna_seq:
            return ""
        rna = rna_seq.upper().replace(" ", "")
        prot = []
        # Recorrer la secuencia en pasos de 3 (codones)
        for i in range(0, len(rna) - 2, 3):
            codon = rna[i:i+3]
            aa = self.codon_table.get(codon, "?")
            if aa == "*":
                break
            prot.append(aa)
        return "".join(prot)
