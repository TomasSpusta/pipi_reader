
from getmac import get_mac_address as gma  # module for mac adress
from subprocess import check_output #module for ip address

class User:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class Instrument:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        



class Token:
    def __init__(self, string: str, expiration: str):
        self.string = string
        self.expiration = expiration

    def to_dict(self):
        return {
            "string": self.string,
            "expiration": self.expiration
        }

class Mac_Ip:
    def __init__(self, mac: str, ip: str):
        self.mac = mac
        self.ip = ip
        
    def fetch_mac (self):
        try:
            self.mac = gma()  
            print("My MAC adress is: {}".format(self.mac))
            return self.mac

        except Exception as mac_e:
            print("Get MAC error: " + str(mac_e))
            
    def fetch_ip (self):
        try:
            self.ip = check_output(['hostname', '-I']) 
            print("My IP adress is: {}".format(self.ip))
            return self.ip

        except Exception as mac_e:
            print("fetch ip error: " + str(mac_e))