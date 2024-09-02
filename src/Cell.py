import emoji

class Cell:
    def __init__(self):
        self._status = 'empty'
        self._image = emoji.emojize("⬜")

    def get_status(self):
        return self._status

    def get_image(self):
        return self._image

    def set_status(self, new_status):
        if self._status != 'empty' and \
                new_status != 'empty' and \
                self._status != new_status:
            raise Exception("Эта клетка уже занята")
        self._status = new_status
        if new_status == 'O':
            self._image = emoji.emojize("⭕")
        elif new_status == 'X':
            self._image = emoji.emojize("❌")
        else:
            self._image = emoji.emojize("⬜")
        return self
