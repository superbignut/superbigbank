from abc import ABCMeta, abstractmethod



class DataHandler(metaclass=ABCMeta):

    @abstractmethod
    def get_pre_bars(self):
        raise NotImplementedError("get_pre_bars method must be implemented!")

    @abstractmethod
    def get_current_bar(self):
        raise NotImplementedError("get_current_bars method must be implemented!")
