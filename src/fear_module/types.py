from abc import ABC
from enum import Enum

from pyrogram import filters
from pyrogram.handlers import BusinessConnectionHandler, BusinessMessageHandler, Handler


class ClientType(Enum):
    USER = "User"
    BOT = "Bot"


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
        return f"{self.prefix}{self.name} - {self.description}"

    def add_handler(self, handler: Handler):
        if (
            isinstance(handler, (BusinessConnectionHandler, BusinessMessageHandler))
            and self.client_type == ClientType.USER
        ):
            raise ValueError("Business handlers are not supported for USER client.")
        self.handlers.append(handler)


class FearModule(ABC):
    name: str = "undefined"
    version: str = "1.0.0"
    author: str = "Name"

    def __init__(self):
        self._commands: list[Command] = []
        self._handlers: list[Handler] = []

    @property
    def commands(self):
        return f"-- {type(self).name} ({type(self).version}) --\n" + "\n".join(
            command.info for command in self._commands
        )

    @property
    def handlers(self):
        handlers: list[Handler] = []
        for command in self._commands:
            handlers.extend(command.handlers)
        handlers.extend(self._handlers)
        return handlers

    def add_command(self, command: Command):
        self._commands.append(command)

    def add_handler(self, handler: Handler):
        self._handlers.append(handler)
