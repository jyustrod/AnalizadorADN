# Lector básico de archivos FASTA

class FastaLoader:
    # Almacenar el nombre del archivo y las secuencias cargadas
    def __init__(self, filename=None):
        self.filename = filename
        # Almacenar las secuencias como {encabezado: secuencia}
        self.sequences = {}

    def load_fasta(self, filename=None):
        # Cargar el archivo FASTA y rellenar self.sequences
        # Utilizar un lector simple que cubre los casos más comunes
        if filename:
            self.filename = filename
        if not self.filename:
            raise ValueError("No se indicó el nombre del archivo FASTA")

        self.sequences = {}
        current_header = None
        current_seq_parts = []

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if not line:
                        # Ignorar líneas vacías
                        continue
                    if line.startswith(">"):
                        # Al detectar un nuevo encabezado, guardar el anterior si corresponde
                        if current_header is not None:
                            seq = "".join(current_seq_parts).replace(" ", "").upper()
                            # Evitar sobrescribir encabezados repetidos agregando un sufijo numerado
                            header_to_use = current_header
                            i = 2
                            while header_to_use in self.sequences:
                                header_to_use = "{}__{}".format(current_header, i)
                                i += 1
                            self.sequences[header_to_use] = seq
                        # Iniciar un nuevo bloque para el encabezado actual
                        current_header = line[1:].strip() or "sin_nombre"
                        current_seq_parts = []
                    else:
                        # Acumular líneas de secuencia
                        current_seq_parts.append(line)
                # Al finalizar, guardar la última secuencia pendiente si existe
                if current_header is not None:
                    seq = "".join(current_seq_parts).replace(" ", "").upper()
                    header_to_use = current_header
                    i = 2
                    while header_to_use in self.sequences:
                        header_to_use = "{}__{}".format(current_header, i)
                        i += 1
                    self.sequences[header_to_use] = seq
        except FileNotFoundError:
            # Manejar error de archivo inexistente
            raise FileNotFoundError("No se encontró el archivo: {}".format(self.filename))
        except UnicodeDecodeError:
            # Reintentar con manejo básico de errores de codificación
            with open(self.filename, "r", errors="ignore") as f:
                current_header = None
                current_seq_parts = []
                for raw_line in f:
                    line = raw_line.strip()
                    if not line:
                        continue
                    if line.startswith(">"):
                        if current_header is not None:
                            seq = "".join(current_seq_parts).replace(" ", "").upper()
                            header_to_use = current_header
                            i = 2
                            while header_to_use in self.sequences:
                                header_to_use = "{}__{}".format(current_header, i)
                                i += 1
                            self.sequences[header_to_use] = seq
                        current_header = line[1:].strip() or "sin_nombre"
                        current_seq_parts = []
                    else:
                        current_seq_parts.append(line)
                if current_header is not None:
                    seq = "".join(current_seq_parts).replace(" ", "").upper()
                    header_to_use = current_header
                    i = 2
                    while header_to_use in self.sequences:
                        header_to_use = "{}__{}".format(current_header, i)
                        i += 1
                    self.sequences[header_to_use] = seq

        # Validar formato básico del archivo
        if not self.sequences:
            raise ValueError("El archivo FASTA parece estar vacío o mal formateado")
        return self.sequences

    def get_sequences(self):
        # Devolver las secuencias cargadas
        return self.sequences
