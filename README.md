# Fear Module SDK

`fear-module` is the Python 3.14+ SDK for modules loaded by [Fear](https://github.com/Fear-Selfbot/fear). It provides `FearModule`, `Command`, `ClientType`, Telegram client types, and protocols describing the host application.

The SDK uses the standard Python `logging` hierarchy under `fear_module.*` and does not configure global handlers or log levels. The host application controls logging configuration.

Modules subclass `FearModule`, accept a host client, register commands with `add_commands()`, and attach Kurigram handlers through `Command.add_handler()` or `add_handlers()`. The host is responsible for importing modules and connecting handlers to its user and bot clients. `FearClientProtocol` is the host contract; `FearClient` is retained as a compatibility scaffold and raises `NotImplementedError` for host operations.

See [SDK API and example](docs/api.md), [review status](docs/code-review.md), and Fear's [module authoring guide](https://github.com/Fear-Selfbot/fear/blob/main/docs/modules.md).

## Development checks

```sh
uv run --locked python -m unittest discover -s tests -v
uv lock --check
```
