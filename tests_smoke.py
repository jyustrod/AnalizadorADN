# Pequeña prueba rápida del flujo principal (no interactivo)
from analizador_adn.fasta_loader import FastaLoader
from analizador_adn.sequence_analyzer import SequenceAnalyzer
from analizador_adn.pattern_finder import PatternFinder
from analizador_adn.translator import Translator
from analizador_adn.mutator import Mutator

# Armo un FASTA chico en memoria (simularé cargándolo desde un archivo temporal)
import os, tempfile

data = ">seq1\nATGCGTATATTT\n>seq2\nGGGCCCtttAAA\n"

fd, path = tempfile.mkstemp(suffix=".fa")
os.close(fd)
with open(path, "w") as f:
    f.write(data)

try:
    loader = FastaLoader()
    seqs = loader.load_fasta(path)
    assert len(seqs) == 2

    analyzer = SequenceAnalyzer(seqs)
    lengths = analyzer.sequence_length()
    counts = analyzer.count_nucleotides()
    gc = analyzer.gc_content()

    # chequeos básicos
    assert lengths
    assert counts
    assert gc

    finder = PatternFinder(seqs)
    pats = finder.find_pattern("AT")
    reps = finder.find_repeats(2)
    mot = finder.find_motif("TT")

    # no aseguro contenido específico, solo que existen las claves
    for k in seqs.keys():
        assert k in pats
        assert k in reps
        assert k in mot

    trans = Translator()
    # Traducción simple: seq1 empieza con ATG => M
    rna = trans.transcribe_dna_to_rna(seqs[list(seqs.keys())[0]])
    prot = trans.translate_to_protein(rna)
    assert prot.startswith("M")

    mut = Mutator()
    mutated = mut.random_mutations(seqs[list(seqs.keys())[0]], 3)
    comp = mut.compare_proteins(seqs[list(seqs.keys())[0]], mutated)
    assert "original" in comp and "mutado" in comp
finally:
    os.remove(path)

print("SMOKE OK")

