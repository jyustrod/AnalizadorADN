from __future__ import annotations


# Traducir ADN→ARN y ARN→Proteína
class Translator:
    def __init__(self):
        # Diccionario (tabla) de codones a aminoácidos; las claves son tripletes (UUU, AUG, ...)
        # y los valores son letras de aminoácidos (formato 1 letra). '*' se usa como STOP (paro).
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
            # STOP (paro)
            "UAA": "*", "UAG": "*", "UGA": "*",
        }

    def transcribe_dna_to_rna(self, dna_seq):
        # Pasar de ADN a ARN es básicamente cambiar T por U; también se quitan espacios y saltos de línea
        if dna_seq is None:
            return ""
        return (dna_seq.upper().replace("T", "U").replace("\n", "").replace(" ", ""))

    def translate_to_protein(self, rna_seq):
        # Recorrer la cadena en pasos de 3 (codones) y mapear a aminoácidos usando la tabla
        # Si se ve un STOP ('*'), se corta la traducción (break)
        if not rna_seq:
            return ""
        rna = rna_seq.upper().replace(" ", "")
        prot = []
        for i in range(0, len(rna) - 2, 3):  # range con paso de 3
            codon = rna[i:i+3]
            aa = self.codon_table.get(codon, "?")  # '?' indica codón desconocido
            if aa == "*":
                break
            prot.append(aa)
        return "".join(prot)
