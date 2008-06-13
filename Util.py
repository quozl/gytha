def strnul(input):
    """ convert a NUL terminated string to a normal string
    """
    return input.split('\000')[0]

