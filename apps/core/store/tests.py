import pytest
from .store_code_gen import StoreCodeGen

user_seed = 1234


def assert_store_code(code, fst_len=9):
    """
    Helper function that asserts the code has the correct format.
    :param code: The generated code
    :param fst_len: The length of the first section of the code
    """
    snd_len = len(code)
    assert code[:fst_len].isnumeric() and code[fst_len:snd_len].isalpha()

#
# LENGTH SECTION
#

@pytest.mark.parametrize("len_fst, len_snd", [
    (5, 1),  # Tests for 5 first charset digits and 1 second charset letter
    (3, 3),  # Tests for 3 first charset digits and 3 second charset letters
    (2, 5),  # Tests for 2 first charset digits and 5 second charset letters
    (1, 1),  # Tests for 1 first charset digit and 1 second charset letter
])
def test_uni_varying_length_sections_returns_correct_format(len_fst, len_snd):
    """
    Test function that verifies if the generated store code has the correct format for varying
    lengths of the first and second sections.
    :param len_fst: The length of the first section
    :param len_snd: The length of the second section
    """
    storecode = StoreCodeGen(user_seed=user_seed, len_first_charset=len_fst, len_second_charset=len_snd)
    assert_store_code(storecode.gen_storecode(), len_fst)


@pytest.mark.parametrize("len_fst, len_snd", [
    (0, 0),  # Tests for zero-length first and second charset, which raises a value error
    (1, 0),  # Tests for first charset with length of 1 and second charset with length of 0
    (0, 1),  # Tests for first charset with length of 0 and second charset with length of 1
])
def test_uni_zero_length_raises_value_error(len_fst, len_snd):
    """
    Test function that verifies if the constructor raises a ValueError when the length of the
    first and/or second charset is zero.
    :param len_fst: The length of the first section
    :param len_snd: The length of the second section
    """
    with pytest.raises(ValueError):
        StoreCodeGen(user_seed=user_seed, len_first_charset=len_fst, len_second_charset=len_snd)


#
# BASE35 ENCODING
#

charset = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"


@pytest.mark.parametrize("v, base, ch_set, length, answer",
    [(x, len(charset), charset, 1, y) for x, y in enumerate(charset)]
)
def test_uni_encoding_base_35_1_length_words_returns_base35_alpha_1_length_words(
        v, base, ch_set, length, answer):
    """
    Test function that verifies if the encoding function returns the expected base-35
    alpha-numeric character for a one-digit number.
    :param v: The number to encode
    :param base: The base of the encoding
    :param ch_set: The charset to use for the encoding
    :param length: The length of the encoding
    :param answer: The expected result of the encoding
    """
    storecode = StoreCodeGen(user_seed=user_seed)
    assert storecode.encode_section(v, base, ch_set, length) == answer


def gen_2_length_base_35_word():
    """
    Helper function that generates a list of base-35 alpha-numeric words of length 2.
    :return: A list of base-35 alpha-numeric words of length 2
    """
    res = list()
    for x in charset[1:]:
        for y in charset:
            res.append(x + y)

    return res


@pytest.mark.parametrize("v, base, ch_set, length, answer",
    [(x, len(charset), charset, 2, y) for x, y in enumerate(gen_2_length_base_35_word(), 35)]
)
def test_uni_encoding_base_35_2_length_words_returns_base35_alpha_2_len_words(
        v, base, ch_set, length, answer):
    """
    Test function that verifies if the encoding function returns the expected base-35
    alpha-numeric character for a two-digit number.
    :param v: The number to encode
    :param base: The base of the encoding
    :param ch_set: The charset to use for the encoding
    :param length: The length of the encoding
    :param answer: The expected result of the encoding
    """
    storecode = StoreCodeGen(user_seed=user_seed)
    assert storecode.encode_section(v, base, ch_set, length) == answer

#
# GEN_TKC WITH PREFIX
#


@pytest.mark.parametrize("prefix",
    ['H2Oz', 'TNT', 'PREFIX', 'VERY_LONG_PREFIX', '']
)
def test_uni_varying_prefix_returns_prefix(prefix):
    """
    Test function that verifies if the generated store code with a varying prefix
    starts with the expected prefix and has the correct format.
    :param prefix: The prefix to add to the store code
    """
    storecode = StoreCodeGen(user_seed=user_seed)
    assert prefix == storecode.gen_storecode(prefix)[:len(prefix)]
    assert_store_code(storecode.gen_storecode(prefix)[len(prefix):])
