class MOTD:
    """ message of the day """
    def __init__(self):
        self.list = []

    def add(self, text):
        self.list.append(text)

    def get(self):
        return self.list

