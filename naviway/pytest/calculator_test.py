# calculator_test.py
import pytest
from .calculator import add, subtract
from django import urls
from navigator.naviway.views2 import check_navi

def test_add():
    firstNumber = 9
    secondNumber = 2
    assert add(firstNumber, secondNumber) == 11


def test_subtract():
    firstNumber = 7
    secondNumber = 2
    assert subtract(firstNumber, secondNumber) == 5

def test_check_navi():
    assert check_navi() == 200

@pytest.mark.django_db
def test_reg_us():
    pass

