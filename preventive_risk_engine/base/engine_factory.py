"""Factory that builds the configured top-level engine by name."""

from typing import Any


class EngineFactory:
    _registry: dict = {}

    @classmethod
    def register(cls, name: str, engine_cls):
        cls._registry[name] = engine_cls

    @classmethod
    def create(cls, name: str, config: Any):
        if name not in cls._registry:
            raise KeyError(f"No engine registered under '{name}'. Known: {list(cls._registry)}")
        return cls._registry[name](config)
