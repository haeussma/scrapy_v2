
from abc import ABC, abstractmethod


class test(ABC):

    def count_in_range(self):
        return "[i for i in range(7)]"

    @abstractmethod
    def multiply():
        pass


class test_a(test):
    def __init__(self, number:int) -> None:
        self.number = number
        self.rang: str = super().count_in_range()

    def print_hi(self):
        return f"hi, my number is {self.number}"

    def multiply(self):
        return 10*self.number



print(test_a(6).rang)