import ipaddress

class General:
    retest_time:str
    max_hops   :str
    timeout    :str

    def __init__(self,
                 retest  :str = "5",
                 max_hops:str = "15",
                 time    :str = "1"
                 ):
        self.retest_time = retest
        self.max_hops = max_hops
        self.timeout = time


class TestConfig:
    gateway    :str
    destination:str
    port       :str
    protocol   :str

    def __init__(self,
                 gate:str,
                 dest:str,
                 port:str,
                 prot:str):

        self.gateway = gate
        self.destination = dest
        self.port = port
        self.protocol = prot

    def check(self, index):
        if self.protocol == "icmp":
            return True
        elif int(self.port) >= 1 & int(self.port) <= 65535:
            if self.protocol == "tcp" or self.protocol == "udp":
                return True
        print(f'Error: test_{index} is invalid!')
        return False