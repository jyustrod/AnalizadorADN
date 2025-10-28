# Lector básico de archivos FASTA

# En Python, un fichero FASTA tiene líneas que empiezan por '>' (encabezado)
# y luego líneas con la secuencia. Aquí se guardan como {encabezado: secuencia}
class FastaLoader:
    # __init__ guarda el nombre de archivo y un dict vacío para las secuencias
    def __init__(self, filename=None):
        self.filename = filename
        self.sequences = {}

    def load_fasta(self, filename=None, progress_callback=None):
        # Permitir pasar el nombre aquí o en el constructor
        if filename:
            self.filename = filename
        if not self.filename:
            raise ValueError("No se indicó el nombre del archivo FASTA")

        # Reiniciar el diccionario de secuencias
        self.sequences = {}
        current_header = None
        current_seq_parts = []  # lista de trozos de secuencia que luego se unirán
        headers_count = 0
        lines_count = 0

        def _report_progress(f):
            if progress_callback:
                bytes_read = 0
                try:
                    # En modo texto, tell suele devolver el offset de bytes consumidos
                    bytes_read = f.tell()
                except Exception:
                    try:
                        bytes_read = f.buffer.tell()
                    except Exception:
                        bytes_read = 0
                try:
                    progress_callback(headers_count, bytes_read, lines_count)
                except Exception:
                    # No romper la carga si el callback falla
                    pass

        try:
            # with abre el fichero y lo cierra automáticamente al salir del bloque
            with open(self.filename, "r", encoding="utf-8") as f:
                for raw_line in f:  # recorrer línea a línea
                    lines_count += 1
                    line = raw_line.strip()  # strip quita espacios y saltos de línea
                    if not line:
                        # saltar líneas vacías
                        continue
                    if line.startswith(">"):
                        # Al ver un encabezado nuevo, guardar el anterior si hubiera
                        if current_header is not None:
                            seq = "".join(current_seq_parts).replace(" ", "").upper()
                            # Evitar sobrescribir: si ya existe el mismo encabezado, añadir sufijo __2, __3, ...
                            header_to_use = current_header
                            i = 2
                            while header_to_use in self.sequences:
                                header_to_use = "{}__{}".format(current_header, i)
                                i += 1
                            self.sequences[header_to_use] = seq
                        # Guardar el nuevo encabezado (sin el '>') y resetear acumulador
                        current_header = line[1:].strip() or "sin_nombre"
                        current_seq_parts = []
                        headers_count += 1
                        if headers_count % 100 == 0:
                            _report_progress(f)
                    else:
                        # Acumular trozos de secuencia tal cual (luego se normaliza a mayúsculas)
                        current_seq_parts.append(line)
                # Al acabar el fichero, no olvidar guardar el último bloque
                if current_header is not None:
                    seq = "".join(current_seq_parts).replace(" ", "").upper()
                    header_to_use = current_header
                    i = 2
                    while header_to_use in self.sequences:
                        header_to_use = "{}__{}".format(current_header, i)
                        i += 1
                    self.sequences[header_to_use] = seq
                # Informe final
                _report_progress(f)
        except FileNotFoundError:
            # Error típico: ruta incorrecta o archivo inexistente
            raise FileNotFoundError("No se encontró el archivo: {}".format(self.filename))
        except UnicodeDecodeError:
            # Si hay lío con la codificación (UTF-8), leer ignorando errores
            with open(self.filename, "r", errors="ignore") as f:
                current_header = None
                current_seq_parts = []
                for raw_line in f:
                    lines_count += 1
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
                        headers_count += 1
                        if headers_count % 100 == 0:
                            _report_progress(f)
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
                _report_progress(f)

        # Comprobar que se ha leído algo con sentido
        if not self.sequences:
            raise ValueError("El archivo FASTA parece estar vacío o mal formateado")
        return self.sequences

    def get_sequences(self):
        # Devolver el dict con las secuencias
        return self.sequences
