from random import random, seed
import string

class StoreCodeGen(object):
    
    # Initialize the object with user-provided or default values
    def __init__(
        self,
        user_seed=None,  # User-provided seed for the random number generator
        len_first_charset=9,  # Length of the first charset
        len_second_charset=4,  # Length of the second charset
        base=36,  # Base used for encoding
        first_charset=string.digits,  # First charset used for encoding
        second_charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ"  # Second charset used for encoding
    ):
        # Seed the random number generator
        seed(a=user_seed)
        # Prime number used for generating random numbers
        self.prime_num = 1679979167
        # Set the first and second charset
        self.first_charset = first_charset
        self.second_charset = second_charset

        # Check that len_first_charset and len_second_charset are greater than 1
        if len_first_charset < 1 or len_second_charset < 1:
            raise ValueError("len_fst or len_snd must be greater than 1")

        # Set the length of the first and second charset
        self.len_first_charset = len_first_charset
        self.len_second_charset = len_second_charset
        # Set the base used for encoding
        self.base = base

    # Generate a random number using the random number generator
    def get_random_number(self):
        return int((random() * self.prime_num) % (36 ** 6))

    # Encode a number using the provided base and charset
    def encode_section(
        self,
        v: int,  # The number to encode
        base: int,  # The base to use for encoding
        charset: str,  # The charset to use for encoding
        section_len: int  # The length of the encoding
    ):
        # Initialize the result as an empty list
        result = []
        c = 0
        # Encode the number using the provided base and charset until the desired length is reached
        while c < section_len and v >= 0:
            v, remainder = divmod(v, base)
            result.append(charset[remainder])
            c += 1
        # Reverse the result and join the characters together into a string
        result.reverse()
        return ''.join(result)

    # Generate a store code with an optional prefix
    def gen_storecode(self, prefix=''):
        # Generate a random number
        num = self.get_random_number()
        # Encode the first section using the first charset and length
        first_section = self.encode_section(
            num,
            len(self.first_charset),
            self.first_charset,
            self.len_first_charset
        )
        # Encode the second section using the second charset and length
        second_section = self.encode_section(
            num,
            len(self.second_charset),
            self.second_charset,
            self.len_second_charset
        )
        # If a prefix is provided, concatenate the prefix, first section, and second section
        if prefix:
            return '%s%s%s' % (prefix, first_section, second_section)
        # Otherwise, concatenate only the first and second sections
        else:
            return '%s%s' % (first_section, second_section)
