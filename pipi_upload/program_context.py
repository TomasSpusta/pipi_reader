from model_classes import Instrument, User, Token, Session


class ProgramStateContext:
    def __init__(self):
        self.instrument: Instrument = None
        self.user: User = None
        self.session: Session = None
        self.token: Token = None  # Placeholder for Token
        self.random_phrase = "Push the boundaries!"
