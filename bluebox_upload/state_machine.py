from transitions import Machine


class ProgramState:
    states = [
        "waiting",
        "checking_user",
        "checking_reservation",
        "in_session",
        "loading",
        "user_ok",
        "user_nok",
        "reservation_ok",
        "reservation_nok",
        "button_menu",
        "reservation_prolonged",
        "session_ended_by_user",
        "session_ended",
        "checking_token",
    ]


class StateMachine:
    def __init__(self):
        self.machine = Machine(
            model=self, states=ProgramState.states, initial="waiting"
        )

        self.machine.add_transition("start_session", "waiting", "checking_user")
        self.machine.add_transition("validate_user", "checking_user", "user_ok")
        self.machine.add_transition("invalidate_user", "checking_user", "user_nok")
        self.machine.add_transition(
            "confirm_reservation", "checking_reservation", "reservation_ok"
        )
        self.machine.add_transition(
            "deny_reservation", "checking_reservation", "reservation_nok"
        )
        self.machine.add_transition(
            "prolong_reservation", "reservation_ok", "reservation_prolonged"
        )
        self.machine.add_transition(
            "end_session_by_user", "in_session", "session_ended_by_user"
        )
        self.machine.add_transition("end_session", "loading", "session_ended")
        self.machine.add_transition(
            "reset",
            ["session_ended", "session_ended_by_user", "reservation_nok", "user_nok"],
            "waiting",
        )
        self.machine.add_transition("start_token_check", "waiting", "checking_token")
        self.machine.add_transition("token_validated", "checking_token", "waiting")
        self.machine.add_transition("token_invalid", "checking_token", "waiting")
