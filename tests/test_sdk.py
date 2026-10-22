import unittest
from types import SimpleNamespace

from pyrogram.handlers import MessageHandler

from fear_module import ClientType, Command, FearClient, FearModule


async def handler(client, message):
    return None


class ExampleModule(FearModule):
    name = "Example"


class FearModuleTests(unittest.TestCase):
    def setUp(self):
        self.client = SimpleNamespace(user=object(), bot=object(), modules=[])
        self.module = ExampleModule(self.client)

    def test_command_handler_is_returned_only_for_its_client_type(self):
        command = Command("ping", ".", "Check response", ClientType.USER)
        registered = MessageHandler(handler, command.filter)
        command.add_handler(registered)
        self.module.add_commands(command)

        self.assertEqual(self.module.get_handlers(ClientType.USER), [registered])
        self.assertEqual(self.module.get_handlers(ClientType.BOT), [])

    def test_module_handlers_follow_module_client_type(self):
        registered = MessageHandler(handler)
        self.module.add_handlers(registered)

        self.assertEqual(self.module.user_handlers, [registered])
        self.assertEqual(self.module.bot_handlers, [])

    def test_host_client_stub_does_not_silently_succeed(self):
        with self.assertRaises(NotImplementedError):
            FearClient().load_modules()


if __name__ == "__main__":
    unittest.main()
