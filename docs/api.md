# Fear Module SDK

## Назначение

`fear-module` — SDK для написания модулей, которые загружает Fear. Пакет требует Python 3.14+ и Kurigram `>=2.2.26`; backend сборки — `uv_build`. Публичные экспорты: `ClientType`, `Command`, `FearBot`, `FearClient`, `FearModule`, `FearUser`.

SDK использует стандартные логгеры `fear_module.*` и пишет диагностические события уровня DEBUG при регистрации команд и обработчиков. Настройку уровня и handlers оставляет хосту.

## Команды и обработчики

`Command(name, prefix="/", description="", clientType=ClientType.USER)` создаёт фильтр Kurigram через `command.filter`, строку справки через `command.info` и список обработчиков. `add_handler()` добавляет обработчик. `FearModule` принимает хост-клиент в конструкторе, хранит команды через `add_commands()` и общие обработчики через `add_handlers()`. Реализация фильтрует команды и обработчики по `ClientType`.

Типы клиента: `USER`, `BOT`, `SECRETARY`. Хост Fear подключает `SECRETARY`-обработчики к своему bot-клиенту. Переопределите `register()` для настройки команд/обработчиков при каждой загрузке. Сам SDK не загружает модули и не управляет Telegram-клиентами. `FearClientProtocol` описывает контракт хоста; экспортируемый `FearClient` оставлен как совместимый каркас и его методы завершаются `NotImplementedError`.

```python
from fear_module import Command, FearModule
from pyrogram.handlers import MessageHandler

hello = Command("hello", ".", "Ответить приветствием")

async def hello_handler(client, message):
    await message.edit("Привет")

class HelloModule(FearModule):
    name = "Hello"

    def register(self):
        hello.add_handler(MessageHandler(hello_handler, hello.filter))
        self.add_commands(hello)
```

Поместите класс модуля в `main.py` каталога `src/modules/<name>/` приложения Fear. Конструктор модуля должен принимать клиент и передавать его в `super().__init__(client)`.

## Сборка и текущее состояние

Проверки разработки: `python -m compileall -q src tests`, `uv lock --check`, `uv run --locked python -m unittest discover -s tests -v`, `ty check`. Инструкции хоста и его сценарий загрузки описаны в документации репозитория Fear.
