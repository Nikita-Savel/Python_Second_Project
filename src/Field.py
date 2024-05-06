from src.Cell import Cell
from src import Globals


class Field:
    def __init__(self, sz=3):
        self._size = Globals.size
        self._arr = []
        for i in range(sz):
            tmp = []
            for j in range(sz):
                tmp.append(Cell())
            self._arr.append(tmp)

    def set_symbol(self, x, y, symbol):
        return self._arr[x][y].set_status(symbol)

    def get_cell_status(self, x, y):
        return self._arr[x][y].get_status()

    def get_cell_image(self, x, y):
        return self._arr[x][y].get_image()
    
    def get_size(self):
        return self._size
