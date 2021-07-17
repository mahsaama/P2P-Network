
class Chatroom:
    def __init__(self, starter_chat_name: str, starter_id: int):
        self.possible_members = [starter_id]
        self.members = {starter_id: starter_chat_name}