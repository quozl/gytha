class MOTD:
    """ message of the day """
    def __init__(self):
        self.list = []

    def add(self, text):
        self.list.append(text)
        # FIXME: SP_MOTD has a separator between human text and server
        # generated defaults, and the separator looks odd when
        # displayed.
        # \t@@@

    def get(self):
        return self.list

