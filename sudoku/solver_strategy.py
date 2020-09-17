"""
solver_strategy.py module
"""
from queue import Queue, LifoQueue
from abc import ABC, abstractmethod


class SearchStrategy(ABC):
    """
    abstract search strategy class
    """
    @abstractmethod
    def __str__(self):
        pass

    @staticmethod
    @abstractmethod
    def get_strategy():
        """
        abstract get strategy method
        :return:
        """


class BreadthFirstSearchStrategy(SearchStrategy):
    """
    breadth first search concrete strategy class
    """

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def get_strategy():
        """
        get strategy static method
        :return:
        """
        return Queue()


class DepthFirstSearchStrategy(SearchStrategy):
    """
    depth first search concrete strategy class
    """

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def get_strategy():
        """
        get strategy static method
        :return:
        """
        return LifoQueue()


class SearchStrategyFactory:
    """
    search strategy factory
    """

    def __init__(self, strategy_type):
        self.strategy_type = strategy_type

    def __repr__(self):
        return self.__class__.__name__

    def get_strategy(self):
        """
        get concrete search strategy method
        :return:
        """
        return self.strategy_type.get_strategy()
