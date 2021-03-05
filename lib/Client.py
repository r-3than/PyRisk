class Client:
    def __init__(self,conn,addr):
        self.conn = conn #socket connection object
        self.addr = addr #address
        self.IsOnline = False # are they online
