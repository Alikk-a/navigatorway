from ..models import Page, Texniki, Targetteh, Podhod, Targ, Cursceteh, Cursce
from ..views import check_navi
# from django.shortcuts import render, get_object_or_404
# import requests
import pytest

# функция ответа сервера из views
def test_check_navi():
    assert check_navi() == 200


test_param = [
    (Cursce, 'name_cource', 'test_Cource'),
    (Targ, 'cel_texniki', 'test_Targ'),
    (Page, 'pagename', '113'),
    (Podhod, 'podhod', 'test_Podhod'),
    (Texniki, 'name', 'test_Texniki'),
    (Targetteh, 'id_cel', 210),
    (Cursceteh, 'id_tex', 777),
]
@pytest.mark.django_db
@pytest.mark.parametrize('model_name, filt, expected', test_param)
def test_check_model(model_name, filt, expected):
    crt_to_db = model_name.objects.create(**{filt: expected})
    get_from_db = model_name.objects.filter(**{filt: expected})
    print(filt)
    print('Грузим: ' + str(expected) + '  Палучаем: ' + str(get_from_db[0].fortest()) + '  тип грузимого - ' + str(type(expected)))
    assert get_from_db[0] == crt_to_db


test_param_dop = [
    (Texniki, 'age', 'preschool'),
]
@pytest.mark.django_db
@pytest.mark.parametrize('model_name, filt, expected', test_param_dop)
def test_check_model_dop(model_name, filt, expected):
    crt_to_db = model_name.objects.create(**{filt: expected}, kol_people='bin', sex='w')
    get_from_db = model_name.objects.filter(**{filt: expected})
    print(filt)
    print('Грузим: ' + str(expected) + '  Палучаем: ' + str(get_from_db[0].agehuman()) + '  тип грузимого - ' + str(type(expected)))
    print('Палучаем: ' + str(get_from_db[0].peoplehuman()) + '  тип грузимого - ' + str(type(expected)))
    print('Палучаем: ' + str(get_from_db[0].sexhuman()) + '  тип грузимого - ' + str(type(expected)))
    assert get_from_db[0].agehuman() == 'для дошкольников'
    assert get_from_db[0].peoplehuman() == 'в паре'
    assert get_from_db[0].sexhuman() == 'для женщин'

"""С помощью маркера xfail мы указываем pytest запустить тестовую функцию, но ожидаем, что она потерпит неудачу.
X для XFAIL, что означает «ожидаемый отказ (expected to fail)». Заглавная X предназначен для XPASS или «ожидается, что он не сработает, но пройдет (expected to fail but passed.)»
"""
@pytest.mark.xfail()
@pytest.mark.django_db
def test_check_notsex():
    crt_to_db = Texniki.objects.create(sex='w')
    get_from_db = Texniki.objects.filter(sex='w')
    assert get_from_db[0].sexhuman() == 'для мужей'

