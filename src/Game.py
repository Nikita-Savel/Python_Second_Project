from src.Player import Player
from src.Field import Field

from aiogram import Bot, Dispatcher, executor, types

class Game:

    def __init__(self, bot, player1, player2, turn):
        self._bot = bot
        self._player1 = player1
        self._player2 = player2
        self._start_game = False
        self._turn = turn
        self._field = Field()

    def step(self, x, y, player):
        try:
            player.make_a_move(x, y, self._field)
            self._turn = 3 - self._turn
        except:
            raise

    def get_cell_image(self, x, y):
        return self._field.get_cell_image(x, y)
    
    def check_end(self):
        temp = []
        for i in range(self._field.get_size()):
            curr = []
            for j in range(self._field.get_size()):
                curr.append(self._field.get_cell_status(i, j))
            temp.append(curr)
        if temp[0][1] == temp[0][2] and temp[0][0] == temp[0][1]:
            if temp[0][1] != 'empty':
                return 'win'
        if temp[1][1] == temp[1][2] and temp[1][0] == temp[1][1]:
            if temp[1][1] != 'empty':
                return 'win'
        if temp[2][1] == temp[2][2] and temp[2][0] == temp[2][1]:
            if temp[2][1] != 'empty':
                return 'win'
        if temp[0][0] == temp[1][0] and temp[1][0] == temp[2][0]:
            if temp[2][0] != 'empty':
                return 'win'
        if temp[0][2] == temp[1][2] and temp[1][2] == temp[2][2]:
            if temp[2][2] != 'empty':
                return 'win'
        if temp[0][1] == temp[1][1] and temp[1][1] == temp[2][1]:
            if temp[2][1] != 'empty':
                return 'win'
        if temp[0][0] == temp[1][1] and temp[1][1] == temp[2][2]:
            if temp[2][2] != 'empty':
                return 'win'
        for i in range(self._field.get_size()):
            for j in range(self._field.get_size()): 
                if temp[i][j] == 'empty':
                   return 'game'
        return 'draw'
        
    def process_press(self, x, y, player):
        if (player == self._player1 and self._turn == 2) or \
              (player == self._player2 and self._turn == 1):
            return 'Не твой ход'
          
        if self._field.get_cell_status(x, y) != 'empty':
            return 'Пчел тут занято'
        
        try:
            self.step(x, y, player)
        except:
            return 'wrong'
        res = self.check_end()
        if res == 'win':
            return 'win' 
        elif res == 'draw':
            return 'draw'
        return 'ok'
