
class RegistrationState():
    def __init__(self):
        self.states = {}

    def set_state(self, chat_id, key, value):
        if chat_id not in self.states:
            self.states[chat_id] = {}
        self.states[chat_id][key] = value

    def get_state(self, chat_id, key):
        if chat_id in self.states and key in self.states[chat_id]:
            return self.states[chat_id][key]
        else:
            return None

    def clear_state(self, chat_id):
        if chat_id in self.states:
            del self.states[chat_id]

registration_state = RegistrationState()
