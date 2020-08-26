class Client:
    def __init__(self,conn,addr):
        self.conn = conn
        self.addr = addr
        self.IsOnline = False
