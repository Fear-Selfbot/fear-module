from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .types import FearModule


class FearClientProtocol(Protocol):
    @property
    def user(self) -> FearUserProtocol: ...

    @property
    def bot(self) -> FearBotProtocol: ...

    @property
    def modules(self) -> list[FearModule]: ...

    def load_modules(self) -> None: ...

    def unload_modules(self) -> None: ...

    def schedule_restart(self) -> None: ...


class FearUserProtocol(Protocol):
    @property
    def client(self) -> FearClientProtocol: ...


class FearBotProtocol(Protocol):
    @property
    def client(self) -> FearClientProtocol: ...
