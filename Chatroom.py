class Chatroom:
    def __init__(self, chat_name: str):
        self.my_name = chat_name
        self.members = {}

    def add_member(self, chat_id: str, chat_name: str = None):
        if not chat_id in self.members or self.members[chat_id] == None:
            self.members[chat_id] = chat_name

    def remove_member(self, chat_id: str):
        if chat_id in self.members:
            return self.members.pop(chat_id)