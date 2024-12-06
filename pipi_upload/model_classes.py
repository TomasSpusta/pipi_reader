


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

