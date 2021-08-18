"""
random
"""
from random import sample, randint


def get_random_sample_from_list(list_of_input_members, count_of_output_members):
    """
    get random sample from a list of integers function
    :param list_of_input_members:
    :param count_of_output_members:
    :return: list of random integers
    """
    return sample(list_of_input_members, count_of_output_members)


def get_randint_from_range(range_start, range_end):
    """
    get random integer from a defined range function
    :param range_start:
    :param range_end:
    :return: random int
    """
    return randint(range_start, range_end)
