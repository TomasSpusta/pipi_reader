# 1. states/base_state.py
from abc import ABC, abstractmethod
from app_context import AppContext


class State(ABC):
    @abstractmethod
    async def run(self, context: AppContext) -> "State":
        pass
