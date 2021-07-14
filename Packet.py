class Packet:
    def __init__(self, typ, src_id, dst_id, data):
        self.type = typ
        self.source_id = src_id
        self.destination_id = dst_id
        self.data = data
