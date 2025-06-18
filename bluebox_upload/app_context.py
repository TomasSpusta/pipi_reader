from dataclasses import dataclass, field
from model_classes import Instrument, Session, Token, User
from screen_manager import Screens
from rfid_reader import RFIDReader
from logger import Logger
from enum import Enum, auto
from api_client import APIClient
from gpiozero import Button


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
    flags: AppFlags = field(default_factory=AppFlags)
    screens: Screens = None
    rfid_reader: RFIDReader = None
    api: APIClient = None
    stop_btn: Button = None
    extend_btn: Button = None
    network_status: dict = None
