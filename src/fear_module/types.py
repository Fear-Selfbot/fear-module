from abc import ABC
from collections.abc import Iterable
from enum import Enum

from pyrogram import Client, filters
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
    SECRETARY = "Secretary"


class Command:
    def __init__(
        self,
        name: str,
        prefix: str = "/",
        description: str = "",
        clientType: ClientType = ClientType.USER,
    ):
        self.prefix = prefix
        self.name = name
        self.description = description
        self.handlers: list[Handler] = []
        self.client_type = clientType

    @property
    def filter(self):
        return filters.command(self.name, self.prefix)

    @property
    def info(self):
        return f"**{self.prefix}{self.name}** - __{self.description}__"

    def add_handler(self, handler: Handler):
        if (
            isinstance(handler, (BusinessConnectionHandler, BusinessMessageHandler))
            and ClientType.USER == self.client_type
        ):
            raise ValueError("Business handlers are not supported for USER client.")
        self.handlers.append(handler)

    def copy_without_handlers(self, clientType: ClientType) -> Command:
        return Command(self.name, self.prefix, self.description, clientType)


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
        return f"> **{type(self).name}** __({type(self).version})__"

    def get_commands(self, client_type: ClientType) -> str:
        return f"{self.header}\n" + "\n".join(
            command.info
            for command in self._commands
            if client_type == command.client_type
        )

    def get_handlers(self, client_type: ClientType) -> list[Handler]:
        handlers = []

        for command in self._commands:
            if client_type == command.client_type:
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
