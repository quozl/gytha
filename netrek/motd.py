"""

message of the day handling.

SP_MOTD packets are received from server.

the first batch of packets arrives during connection, and contain
administrative text flow, terminated by a parameters marker.

the second batch of packets also arrives during connection, and
contain procedural parameter text flow, and are not terminated.  the
batch simply ceases.

subsequent batches of packets arrive on death of a ship, and contain
playing tips relating to the immediately previous ship flight, and are
prefixed with a clear marker.

"""

STATE_INITIAL = 0
STATE_PARAMETERS = 1
STATE_TIPS = 2

MARKER_PARAMETERS = '@@@'
MARKER_CLEAR = 'CLEAR_MOTD'


class MOTD:
    """ message of the day """
    def __init__(self):
        self.list = []
        self.status = STATE_INITIAL

    def add(self, text):
        """ add a line to the list, called on SP_MOTD """
        if MARKER_CLEAR in text:
            self.list = []
            self.status = STATE_TIPS
            return
        if MARKER_PARAMETERS in text:
            self.status = STATE_PARAMETERS
        if self.status in [STATE_INITIAL, STATE_TIPS]:
            self.list.append(text)

    def get(self):
        """ return the list to the caller """
        return self.list

    def tips(self):
        """ return tips to the caller, if tips state was detected """
        if self.status != STATE_TIPS:
            return None
        return self.list
