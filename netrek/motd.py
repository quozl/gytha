STATE_INITIAL=0
STATE_PARAMETERS=1
STATE_TIPS=2

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
            self.status = STATE_TIPS
            return
        if MARKER_PARAMETERS in text:
            self.status = STATE_PARAMETERS
        if self.status in [STATE_INITIAL, STATE_TIPS]:
            self.list.append(text)
        if self.status in [STATE_TIPS]:
            print text

    def get(self):
        return self.list

    def tips(self):
        if self.status != STATE_TIPS:
            return None
        return self.list
