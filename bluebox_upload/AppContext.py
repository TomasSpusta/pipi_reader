from dataclasses import dataclass, field
from model_classes import Instrument, Session, Token, User
from logger import Logger
from enum import Enum, auto


class AppState(Enum):
    INIT = auto()
    WAITING_FOR_CARD = auto()
    VERIFYING_USER = auto()
    STARTING_SESSION = auto()
    IN_SESSION = auto()
    SESSION_ENDED = auto()
    OFFLINE = auto()
    RECOVERED = auto()


@dataclass
class AppFlags:
    lcd_in_use: bool = False
    screen_needs_refresh: bool = False
    block_input: bool = False


@dataclass
class AppContext:
    state: AppState = AppState.INIT
    token: Token = None
    instrument: Instrument = None
    user: User = None
    session: Session = None
    logger: Logger = None
    card_id: str = None
    flags: AppFlags = field(default_factory=AppFlags())
