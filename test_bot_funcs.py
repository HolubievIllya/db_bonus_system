import pytest

from bot import validate_input

def test_normal_2():
    assert validate_input("380998776522 fd", 2) == ["380998776522", "fd"]

def test_normal_4():
    assert validate_input("380998776522 Name Surname 25", 4) == ["380998776522", "Name", "Surname", "25"]

def test_len_mes_bigger_item():
    with pytest.raises(ValueError):
        validate_input("helo fd", 1)

def test_len_mes_shorter_item():
    with pytest.raises(ValueError):
        validate_input("helo fd", 4)

def test_mes0_not_isdigit():
    with pytest.raises(ValueError):
        validate_input("helo fd", 2)

def test_phonenumber_incorrect():
    with pytest.raises(ValueError):
        validate_input("38088992 fd", 2)
        validate_input("38088992321312312 fd", 2)

def test_bonus_incorrect():
    with pytest.raises(ValueError):
        validate_input("380998776522 Name Surname eas", 4)

def test_name_incorrect():
    with pytest.raises(ValueError):
        validate_input("380998776522 32 Surname 32", 4)

def test_surname_incorrect():
    with pytest.raises(ValueError):
        validate_input("380998776522 Name 3232 32", 4)



