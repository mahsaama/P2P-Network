class Chatroom:
    def __init__(self, chat_name: str, id: int):
        self.chat_id = id
        self.my_name = chat_name
        self.members = {}

    def add_member(self, peer_id: str, chat_name: str =None):
        if not peer_id in self.members or self.members[peer_id] == None:
            self.members[peer_id] = chat_name

    def get_definite_members(self):
        definite_members = []
        for m in self.members:
            if self.members[m]:
                definite_members.append(m)
        return definite_members

    def get_peer_chatname(self, peer_id: str):
        if peer_id in self.members:
            return self.members[peer_id]
        raise Exception('peer ID not found in members')

    def remove_member(self, peer_id: str):
        if peer_id in self.members:
            return self.members.pop(peer_id)
