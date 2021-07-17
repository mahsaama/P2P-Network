
class Chatroom:
    def __init__(self, starter_chat_name: str, starter_id: int):
        self.members = {starter_chat_name: starter_id}