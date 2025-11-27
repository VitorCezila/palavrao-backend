from abc import ABC, abstractmethod


class ObjectConverter(ABC):

    @abstractmethod
    def from_dict(self, data: dict):
        pass

    @abstractmethod
    def to_dict(self, obj) -> dict:
        pass
