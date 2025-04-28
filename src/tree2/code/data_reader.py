import pandas

class DataReader:
    def __init__(self, data_source, preload_chunk_size):
        self.data_source = data_source
        self.chunk_size = preload_chunk_size
        self.line_id = 0
        self.value_names = []

    def get_line(self):
        return "placeholder"

class CsvDataReader(DataReader):
    def __init__(self, filename, chunk_size):
        super.__init__(filename)
        self.reader = pandas.read_csv(self.data_source, delimiter=',', quotechar='"', chunksize=self.chunk_size, iterator=True)
        self.value_names = self.reader[0]
        self.chunk_id = 0
        self.chunk = dict()

    def read_chunk(self, chunk_id):
        for i in self.value_names:
            self.chunk[i] = self.reader[i][chunk_id]

    def get_current_line(self):
        result = dict()
        for i in self.value_names:
            result[i] = self.chunk[i]

    def get_next_line(self):
        if self.line_id == 0:
            a =  self.get_current_line()
            self.line_id += 1
        self.line_id += 1
        self.chunk_id = self.line_id // self.chunk_size
        return self.get_current_line()
