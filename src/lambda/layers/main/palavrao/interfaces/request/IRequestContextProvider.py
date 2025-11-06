from abc import ABC, abstractmethod

from palavrao.model.request_context import RequestContext


class IRequestContextProvider(ABC):

    @abstractmethod
    def get_request_context(self) -> RequestContext:
        pass