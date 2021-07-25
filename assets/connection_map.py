
from dataclasses import dataclass, field, fields, astuple, asdict
import dataclasses
from typing import List
from abc import ABC, abstractmethod


import numpy as np


# creating a small abstract class to avoid code duplication
class main_data_class(ABC):
    """main data abstract base class mainly to avoid code duplication and sane defaults

    """


    def __str__(self) -> str:
        """ to handle the terminal call

        Returns:
            str: string to print in an terminal
        """

        string = f'dataclass for connection between nodes with \n {asdict(self)}'
        return string

    def __iter__(self) -> iter:
        """ For loop handling

        Returns:
            iter: iterates through all the "variables"
        """
        return iter(asdict(self).items())

    def get_values(self) -> List:
        """To list the points in the data.

        Returns:
            List: list of all the data points.
        """
        list_data = []
        for i in asdict(self).values():
            list_data += i
        return list_data

    def get_name(self) -> str:
        """TO get the name of the class

        Returns:
            str: name of the class
        """

        return self.__class__.__name__



# I like this a lot for storing information and displaying
@dataclass(frozen=True)
class left_hand(main_data_class):
    """ left hand dataclass which has all the information. with defaults FROZEN

    """

    thumb: List[int] = field(default_factory=lambda:[46, 47, 48, 49, 50])
    index: List[int] = field(default_factory=lambda:[46, 51, 52, 53, 54])
    middle: List[int] = field(default_factory=lambda:[46, 55, 56, 57, 58])
    ring: List[int] = field(default_factory=lambda:[46, 59, 60, 61, 62])
    pinky: List[int] = field(default_factory=lambda:[46, 63, 64, 65, 66])



@dataclass(frozen=True)
class right_hand(main_data_class):
    """ right dataclass which has all the information. with defaults FROZEN

    """

    thumb: List[int] = field(default_factory=lambda:[25, 26, 27, 28, 29])
    index: List[int] = field(default_factory=lambda:[25, 30, 31, 32, 33])
    middle: List[int] = field(default_factory=lambda:[25, 34, 35, 36, 37])
    ring: List[int] = field(default_factory=lambda:[25, 38, 39, 40, 41])
    pinky: List[int] = field(default_factory=lambda:[25, 42, 43, 44, 45])



@dataclass(frozen=True)
class body(main_data_class):

    """ body dataclass which has all the information. with defaults FROZEN

    """

    head: List[int] = field(default_factory=lambda:[17, 15, 0, 1, 0, 16, 18])
    spine: List[int] = field(default_factory=lambda:[1, 8, 5, 1, 2, 12, 8, 9, 5, 1, 2, 8])
    right_arm: List[int] = field(default_factory=lambda:[1, 2, 3, 4])
    left_arm: List[int] = field(default_factory=lambda:[1, 5, 6, 8])
    right_leg: List[int] = field(default_factory=lambda:[8, 9, 10, 11, 22, 23, 11, 24])
    left_leg: List[int] = field(default_factory=lambda:[8, 12, 13, 14, 19, 20, 14, 21])

@dataclass(frozen=True)
class face(main_data_class):

    """ face dataclass which has all the information. with defaults FROZEN

    """
    jaw: List[int] = field(default_factory=lambda:[67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82])
    rBrow: List[int] =  field(default_factory=lambda:[84, 85, 86, 87])
    lBrow: List[int] =  field(default_factory=lambda:[89, 90, 91, 92])
    noseRidge: List[int] =  field(default_factory=lambda:[94, 95, 96])
    noseBot: List[int] = field(default_factory = lambda:[ 98,  99, 100, 101])
    rEye: List[int] = field(default_factory=lambda:[103, 104, 105, 106, 107, 103])
    lEye: List[int] =  field(default_factory=lambda:[109, 110, 111, 112, 113, 109])
    upperLip: List[int] =  field(default_factory=lambda: [115, 116, 117, 118, 119, 120, 130, 129, 128, 127, 115])
    lowerLip: List[int] = field(default_factory=lambda: [127, 131, 132, 133, 121, 122, 123, 124, 125, 115, 127])
    rPupil: List[int] =  field(default_factory=lambda: [135])
    lPupil: List[int] = field(default_factory=lambda:[136])


if __name__ == "__main__":

    left = left_hand()
    for key, value in left:
        print(key, value)
    print(left)

