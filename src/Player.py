class Player:

    def __init__(self, id, name, role=None):
        self._id = id
        self._name = name
        self._role = role
        self._status = 'init'
        self._opponent = None
        self._last_msg = None

    def make_a_move(self, x, y, field):
        try:
            return field.set_symbol(x, y, self._role)
        except:
            raise

    def get_id(self):
        return self._id

    def set_game(self, game):
        self._game = game
        
    def get_name(self):
        return self._name

    def get_status(self):
        return self._status

    def set_status(self, new_status):
        self._status = new_status

    def set_role(self, role):
        self._role = role
    
    def get_role(self):
        return self._role

    def set_opponent(self, opponent):
        self._opponent = opponent

    def get_opponent(self):
        return self._opponent

    def get_game(self):
        return self._game

    def destruct(self):
        self._role = None
        self._status = 'init'
        self._opponent = None
        self._last_msg = None
        self._game = None

    def get_last(self):
        return self._last_msg

    def set_last(self, new_msg):
        self._last_msg = new_msg
        
