
from dataclasses import dataclass

class User:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class Instrument:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

@dataclass
class Session:
    remaining_time:int = 0
    recording_id:str = ""
    reservation_id:str = ""
    warning_sent = False
    ended_by_user = False
    ended_by_time = False


class Token:
    def __init__(self, string: str, expiration: str):
        self.string = string
        self.expiration = expiration

    def to_dict(self):
        return {
            "string": self.string,
            "expiration": self.expiration
        }

