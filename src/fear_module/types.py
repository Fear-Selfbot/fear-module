from abc import ABC
from collections.abc import Iterable
from enum import Enum

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import BusinessConnectionHandler, BusinessMessageHandler, Handler

from .protocols import FearClientProtocol


class FearBot(Client):
    def __init__(self, *args, **kwargs):
        self.client: FearClient
        super().__init__(*args, **kwargs)


class FearUser(Client):
    def __init__(self, *args, **kwargs):
        self.client: FearClient
        super().__init__(*args, **kwargs)


class FearClient:
    def __init__(self, *args, **kwargs):
        self.user: FearUser
        self.bot: FearBot
        self.modules: list[FearModule]

    def unload_modules(self):
        pass

    def load_modules(self):
        pass

    def schedule_restart(self):
        pass


class ClientType(Enum):
    USER = "User"
    BOT = "Bot"


class Command:
    def __init__(
        self,
        name: str,
        prefix: str = "/",
        description: str = "",
        clientTypes: ClientType | list[ClientType] = ClientType.USER,
        scope: ChatType | list[ChatType] | None = None,
    ):
        self.prefix = prefix
        self.name = name
        self.description = description
        self.handlers: list[Handler] = []
        self.client_type = (
            [clientTypes] if isinstance(clientTypes, ClientType) else clientTypes
        )
        self.scope: list[ChatType] = []
        if scope:
            self.scope = [scope] if isinstance(scope, ChatType) else scope

    def check_scope(self, scope: ChatType | None) -> bool:
        if len(self.scope) and scope:
            return scope in self.scope
        return True

    @property
    def filter(self):
        return filters.command(self.name, self.prefix)

    @property
    def info(self):
        return f"{self.prefix}{self.name} - {self.description}"

    def add_handler(self, handler: Handler):
        if (
            isinstance(handler, (BusinessConnectionHandler, BusinessMessageHandler))
            and len(self.client_type) == 1
            and ClientType.USER in self.client_type
        ):
            raise ValueError("Business handlers are not supported for USER client.")
        self.handlers.append(handler)


class FearModule(ABC):
    name: str = "undefined"
    version: str = "1.0.0"
    author: str = "Name"
    client_type: ClientType = ClientType.USER

    def __init__(self, client: FearClientProtocol):
        self.client = client
        self._commands: list[Command] = []
        self._handlers: list[Handler] = []

    @property
    def header(self) -> str:
        return f"{type(self).name} ({type(self).version})"

    def get_commands(
        self, client_type: ClientType, scope: ChatType | None = None
    ) -> str:
        return f"{self.header}\n" + "\n".join(
            command.info
            for command in self._commands
            if client_type in command.client_type and command.check_scope(scope)
        )

    def get_handlers(self, client_type: ClientType) -> list[Handler]:
        handlers = []

        for command in self._commands:
            if client_type in command.client_type:
                handlers.extend(command.handlers)

        if self.client_type == client_type:
            handlers.extend(self._handlers)

        return handlers

    def register(self) -> None:
        """Registrate handlers on start"""

    @property
    def user_handlers(self) -> list[Handler]:
        return self.get_handlers(ClientType.USER)

    @property
    def bot_handlers(self) -> list[Handler]:
        return self.get_handlers(ClientType.BOT)

    @property
    def user_commands(self) -> str:
        return self.get_commands(ClientType.USER)

    @property
    def bot_commands(self) -> str:
        return self.get_commands(ClientType.BOT)

    def add_commands(self, commands: Command | Iterable[Command]):
        if isinstance(commands, Command):
            commands = [commands]
        self._commands.extend(commands)

    def add_handlers(self, handlers: Handler | Iterable[Handler]):
        if isinstance(handlers, Handler):
            handlers = [handlers]
        self._handlers.extend(handlers)
