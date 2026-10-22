from typing import TYPE_CHECKING, Protocol
from collections.abc import Callable

if TYPE_CHECKING:
    from pyrogram.types import User

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

    def schedule_reload(
        self,
        on_success: Callable[[], None] | None = None,
        on_failure: Callable[[Exception], None] | None = None,
    ) -> None: ...


class FearUserProtocol(Protocol):
    @property
    def me(self) -> User | None: ...

    @property
    def client(self) -> FearClientProtocol: ...


class FearBotProtocol(Protocol):
    @property
    def client(self) -> FearClientProtocol: ...
