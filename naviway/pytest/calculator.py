# calculator.py
import requests

def add(firstNumber, secondNumber):
    return firstNumber + secondNumber

def subtract(firstNumber, secondNumber):
    return firstNumber - secondNumber


def check_navi():
    response = requests.get('https://navigatorway.com/')
    print(response.status_code)
    print(response.apparent_encoding)
    print(response.headers)
    return response.status_code

check_navi()