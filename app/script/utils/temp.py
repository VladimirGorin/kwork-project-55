class Temp:
    sleep = 5

    def __init__(self):
        self._global_error = False
        self._listeners = []

    @property
    def global_error(self):
        return self._global_error

    @global_error.setter
    def global_error(self, value):
        if self._global_error != value:
            self._global_error = value
            self.notify_listeners()

    def add_listener(self, listener):
        self._listeners.append(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    def notify_listeners(self):
        for listener in self._listeners:
            listener()


# temp = Temp()
# temp.add_listener(error_handler)
