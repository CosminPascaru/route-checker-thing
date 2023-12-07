import ipaddress

class General:
    retest_time:float
    max_hops   :int
    timeout    :float

    def __init__(self,
                 retest  :float = 5,
                 max_hops:int   = 15,
                 time    :float = 5
                 ):
        self.retest_time = retest
        self.max_hops = max_hops
        self.timeout = time


class TestConfig:
    gateway    :ipaddress
    destination:ipaddress
    port       :int
    protocol   :str

    def __init__(self,
                 gate:ipaddress,
                 dest:ipaddress,
                 port:int,
                 prot:str):

        self.gateway = gate
        self.destination = dest
        self.port = port
        self.protocol = prot

    def check(self, index):
        if self.protocol == "icmp":
            return True
        elif self.port >= 1 & self.port <= 65535:
            if self.protocol == "tcp" or self.protocol == "udp":
                return True
        print(f'Error: test_{index} is invalid!')
        return False