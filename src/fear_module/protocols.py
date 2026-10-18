from typing import Protocol


class FearClientProtocol(Protocol):
    @property
    def user(self) -> FearUserProtocol: ...

    @property
    def bot(self) -> FearBotProtocol: ...

    def load_modules(self) -> None: ...

    def unload_modules(self) -> None: ...


class FearUserProtocol(Protocol):
    client: FearClientProtocol


class FearBotProtocol(Protocol):
    client: FearClientProtocol
