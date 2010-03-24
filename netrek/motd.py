STATE_INITIAL=0
STATE_PARAMETERS=1

MARKER_PARAMETERS='@@@'
MARKER_CLEAR='CLEAR_MOTD'

class MOTD:
    """ message of the day """
    def __init__(self):
        self.list = []
        self.status = STATE_INITIAL

    def add(self, text):
        if MARKER_CLEAR in text:
            self.list = []
            self.status = STATE_INITIAL
            return
        if MARKER_PARAMETERS in text:
            self.status = STATE_PARAMETERS
        if self.status == STATE_INITIAL:
            self.list.append(text)

    def get(self):
        return self.list

