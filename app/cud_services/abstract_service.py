import abc

from sqlmodel import SQLModel


class AbstractService(abc.ABC):
    @abc.abstractmethod
    def create(self, model: SQLModel):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, reference: str, model: SQLModel):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, reference: str):
        raise NotImplementedError
