# Aplicación principal de consola
# Definir el menú y conectar las clases

# Este try/except permite que los imports funcionen en dos escenarios:
# - Como paquete (python -m analizador_adn.app) usando imports relativos (con punto).
# - Ejecutando el archivo suelto (python analizador_adn/app.py) con imports absolutos.
try:
    from .fasta_loader import FastaLoader
    from .sequence_analyzer import SequenceAnalyzer
    from .pattern_finder import PatternFinder
    from .translator import Translator
    from .mutator import Mutator
except Exception:
    # Fallback para ejecución directa: intentar importaciones sin el punto
    from fasta_loader import FastaLoader
    from sequence_analyzer import SequenceAnalyzer
    from pattern_finder import PatternFinder
    from translator import Translator
    from mutator import Mutator


# class define un "molde" para crear objetos con datos (atributos) y funciones (métodos)
class DNAApp:
    # Aquí se gestiona la aplicación en consola
    def __init__(self):
        # __init__ es el "constructor"; self es la propia instancia
        # Se crean las herramientas (otras clases) que se van a usar por el menú
        self.loader = FastaLoader()
        self.analyzer = SequenceAnalyzer()
        self.finder = PatternFinder()
        self.translator = Translator()
        self.mutator = Mutator()

    def _hay_secuencias(self):
        # Devolver True si ya hay secuencias (bool(dict) es True si no está vacío)
        seqs = self.loader.get_sequences()
        return bool(seqs)

    def _refrescar_dependientes(self):
        # Pasar el diccionario de secuencias a las otras clases que lo necesitan
        seqs = self.loader.get_sequences()
        self.analyzer.set_sequences(seqs)
        self.finder.set_sequences(seqs)

    def menu(self):
        # print muestra texto en pantalla; \n es salto de línea
        print("\n===== Analizador de ADN (menú) =====")
        print("1. Cargar archivo FASTA")
        print("2. Análisis del contenido de nucleótidos")
        print("3. Búsqueda de patrones y secuencias de interés")
        print("4. Traducción del ADN a proteínas")
        print("5. Simulación de mutaciones")
        print("6. Salir")

    def opcion_cargar(self):
        # input lee del teclado; strip quita espacios de los extremos
        ruta = input("Ruta del archivo FASTA: ").strip()
        try:
            # Llamar al cargador y luego propagar las secuencias a las demás clases
            seqs = self.loader.load_fasta(ruta)
            self._refrescar_dependientes()
            print("Hecho. Se han cargado {} secuencias.".format(len(seqs)))
        except Exception as e:
            # try/except captura errores y permite informar sin romper el programa
            print("No se ha podido cargar: {}".format(e))

    def opcion_analisis(self):
        if not self._hay_secuencias():
            print("Primero carga un archivo FASTA (opción 1)")
            return
        # Diccionarios devueltos: {encabezado: valor}
        largos = self.analyzer.sequence_length()
        conteo = self.analyzer.count_nucleotides()
        gc = self.analyzer.gc_content()
        print("\n-- Longitudes --")
        for h, L in largos.items():  # for recorre pares clave/valor
            print("{}: {} bases".format(h, L))
        print("\n-- Recuento de nucleótidos --")
        for h, c in conteo.items():
            # Acceso a claves del dict con corchetes
            print("{}: A={} T={} C={} G={} Otros={}".format(h, c['A'], c['T'], c['C'], c['G'], c['N']))
        print("\n-- %GC --")
        for h, g in gc.items():
            print("{}: {}%".format(h, g))

    def opcion_busqueda(self):
        if not self._hay_secuencias():
            print("Primero carga un archivo FASTA (opción 1)")
            return
        print("\n1) Buscar patrón exacto")
        print("2) Buscar repeticiones")
        print("3) Contar motivo")
        sub = input("Elige una subopción (1-3): ").strip()
        if sub == "1":
            pat = input("Patrón a buscar (texto): ").strip().upper()  # upper pasa a mayúsculas
            res = self.finder.find_pattern(pat)
            for h, pos in res.items():
                print("{}: {} hallazgos en posiciones {}".format(h, len(pos), pos))
        elif sub == "2":
            try:
                minimo = int(input("Longitud mínima del repetido: ").strip())  # int convierte a número
            except ValueError:
                print("El mínimo debe ser un número")
                return
            res = self.finder.find_repeats(minimo)
            for h, rep in res.items():
                # rebanado de listas: [:10] muestra como mucho 10 elementos
                vista = rep[:10]
                print("{}: {} repetidos (se muestran 10): {}".format(h, len(rep), vista))
        elif sub == "3":
            mot = input("Motivo a contar: ").strip().upper()
            res = self.finder.find_motif(mot)
            for h, cant in res.items():
                print("{}: {} veces".format(h, cant))
        else:
            print("No he entendido la opción")

    def opcion_traduccion(self):
        if not self._hay_secuencias():
            print("Primero carga un archivo FASTA (opción 1)")
            return
        seqs = self.loader.get_sequences()
        print("Secuencias disponibles:")
        headers = list(seqs.keys())  # list() para ver las claves como lista indexable
        for i, h in enumerate(headers, start=1):  # enumerate da (indice, valor)
            print("{}) {}".format(i, h))
        try:
            idx = int(input("Elige el número de la secuencia: ").strip()) - 1
        except ValueError:
            print("Debe ser un número")
            return
        if idx < 0 or idx >= len(headers):
            print("Número fuera de rango")
            return
        elegido = headers[idx]
        dna = seqs[elegido]
        rna = self.translator.transcribe_dna_to_rna(dna)
        prot = self.translator.translate_to_protein(rna)
        print("\nEncabezado: {}".format(elegido))
        print("ARN (primeros 60): {}{}".format(rna[:60], '...' if len(rna)>60 else ''))
        print("Proteína (primeros 60 aa): {}{}".format(prot[:60], '...' if len(prot)>60 else ''))

    def opcion_mutaciones(self):
        if not self._hay_secuencias():
            print("Primero carga un archivo FASTA (opción 1)")
            return
        seqs = self.loader.get_sequences()
        headers = list(seqs.keys())
        print("Secuencias disponibles:")
        for i, h in enumerate(headers, start=1):
            print("{}) {}".format(i, h))
        try:
            idx = int(input("Elige el número de la secuencia: ").strip()) - 1
        except ValueError:
            print("Debe ser un número")
            return
        if idx < 0 or idx >= len(headers):
            print("Número fuera de rango")
            return
        elegido = headers[idx]
        dna = seqs[elegido]

        print("\n1) Mutación puntual")
        print("2) Mutaciones aleatorias")
        sub = input("Elige una subopción (1-2): ").strip()
        if sub == "1":
            try:
                pos = int(input("Posición (índice 0): ").strip())
                nb = input("Nueva base (A/T/C/G): ").strip().upper()
                mut = self.mutator.point_mutation(dna, pos, nb)
                comp = self.mutator.compare_proteins(dna, mut)
                print("¿Original y mutado son iguales? {}".format(comp['iguales']))
                print("Proteína original (primeros 60): {}".format(comp['original'][:60]))
                print("Proteína mutada   (primeros 60): {}".format(comp['mutado'][:60]))
            except Exception as e:
                print("No se ha podido mutar: {}".format(e))
        elif sub == "2":
            try:
                n = int(input("Cantidad de mutaciones: ").strip())
                mut = self.mutator.random_mutations(dna, n)
                comp = self.mutator.compare_proteins(dna, mut)
                print("¿Original y mutado son iguales? {}".format(comp['iguales']))
                print("Proteína original (primeros 60): {}".format(comp['original'][:60]))
                print("Proteína mutada   (primeros 60): {}".format(comp['mutado'][:60]))
            except Exception as e:
                print("No se ha podido mutar: {}".format(e))
        else:
            print("No he entendido la opción")

    def run(self):
        # while True crea un bucle infinito hasta que se haga break
        while True:
            self.menu()
            # Leer la opción y decidir con if/elif/else qué hacer
            op = input("Elige una opción (1-6): ").strip()
            if op == "1":
                self.opcion_cargar()
            elif op == "2":
                self.opcion_analisis()
            elif op == "3":
                self.opcion_busqueda()
            elif op == "4":
                self.opcion_traduccion()
            elif op == "5":
                self.opcion_mutaciones()
            elif op == "6":
                print("¡Hasta luego! Gracias por usar el analizador.")
                break  # break sale del bucle while y termina la app
            else:
                print("Opción no válida. Prueba de nuevo.")


# Definir una función main para lanzar la app, y proteger con el guard de módulo
# if __name__ == "__main__" significa: solo ejecutar si este archivo es el que se lanza directamente
# (y no cuando se importa desde otro sitio)

def main():
    app = DNAApp()
    app.run()


if __name__ == "__main__":
    main()
