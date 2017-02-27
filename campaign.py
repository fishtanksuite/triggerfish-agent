import threading

class Campaign(object):

    def __init__(self, name=None, data=None):
        self.data = data
        self.name = name
