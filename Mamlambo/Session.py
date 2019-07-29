
import uuid


class Session():

    __enabled = False
    __session_id = None
    __keys = {}

    def __init__(self):
        pass

    def start(self):
        self.__enabled = True
        self.__session_id = str(uuid.uuid4())

    def destroy(self):
        self.__enabled = False

    @property
    def session_id(self):
        return str(self.__session_id)

    @property
    def keys(self):
        if self.__enabled:
            return self.__keys
        else:
            return None

    def __str__(self):
        if self.__enabled:
            return str(self.__keys)
        else:
            return None

    def add(self, key, value):
        self.__keys[key] = value

