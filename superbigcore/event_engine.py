from collections import defaultdict
from queue import Queue
import threading




class Event:

    def __init__(self, event_type):
        pass
        # self.event_type = event_type



class EventEngine:

    def __init__(self):
        self.__queue = Queue() #

        self.__active = False

        self.__thread = None

        self.__handlers = defaultdict(list)


