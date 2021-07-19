class Chatroom:
    def __init__(self, chat_name: str, id: int):
        self.chat_id = id
        self.my_name = chat_name
        self.members = {}
        self.definite_members = {}

    def add_member(self, chat_id: str, chat_name: str = None):
        if not chat_id in self.definite_members or self.definite_members[chat_id] == None:
            self.definite_members[chat_id] = chat_name

    def add_possible_member(self, chat_id: str, chat_name: str = None):
        if not chat_id in self.members or self.members[chat_id] == None:
            self.members[chat_id] = chat_name

    def remove_member(self, chat_id: str):
        if chat_id in self.definite_members:
            return self.members.pop(chat_id)
