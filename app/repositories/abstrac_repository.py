import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, reference):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, reference):
        raise NotImplementedError
