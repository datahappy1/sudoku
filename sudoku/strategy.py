"""
strategy.py module
"""
from queue import Queue, LifoQueue


class Strategy:
    """
    abstract strategy class
    """

    def __init__(self, strategy_type):
        self.strategy_type = strategy_type

    def __repr__(self):
        return self.__class__.__name__

    def get_strategy(self):
        """
        get concrete strategy method
        :return:
        """
        return self.strategy_type.get_strategy()


class BreadthFirstSearchStrategy:
    """
    breadth first search strategy class
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


class DepthFirstSearchStrategy:
    """
    depth first search strategy class
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
