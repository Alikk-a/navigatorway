import pytest
from collections import namedtuple
from django.contrib.auth import get_user_model

from pytest_factoryboy import register
from .factories import UserFactory


register(UserFactory)  # имя фикстуры будет в snakecase виде: user_factory


Person = namedtuple('Person', 'name age')

persons = [
    Person('Ali', 1970),
    Person('Vita', 1977),
]

def id_func(test_data):
    return [f'Person({p.name},{p.age})' for p in test_data]

@pytest.fixture(params=persons, ids=id_func(persons))
def person(request):
    return request.param

@pytest.fixture
def data_1():
    print('\n-data_1')
    return 1


@pytest.fixture(scope='class')  # фикстура выполняется 1 раз До и После всего класса тестов. Еще есть function(умолчание) module и session
def print_hello():
    # raise ConnectionError
    print("\n**Hello")
    yield  # все ниже выполняется ПОСЛЕ теста
    print("\n* END - Hello")

# нижняя часть выводит название теста
@pytest.fixture(autouse=True)  # autouse=True - подключает фикстуру во все тесты
def print_auto(request):
    print("\n фикстура с автозапуском Старт")
    yield
    print(f'\n call test {request.function.__name__} - после теста')

"""
фикстуры для проверки создания и входа пользователя, но у мну не работают, ибо нет функционала авторизации
взято отсюда https://www.youtube.com/watch?v=73kGv8-4Zjk
"""
@pytest.fixture
def user_data():
    print('user_data')
    return {'email': 'user_email', 'name': 'user_name', 'password': 'user_pass113'}

@pytest.fixture
def create_test_user(user_data):
    print('\n-create_test_user')
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    return test_user


"""
тут можно посмотреть основы https://www.youtube.com/watch?v=1HtEPEn4-LY&list=PLlKID9PnOE5hCuNW8L-qxC12U7WPWG6YS

Тестовые файлы должны быть названы test_<something>.py или <something>_test.py.
Методы и функции тестирования должны быть названы test_<something>.
Тестовые классы должны быть названы Test<Something>

запуск конкретного теста в конкретном файле. можно указывать несколько файлов/каталогов/тестов через пробел
pytest navigator/pytest/t_test.py::test_member_access metriktrd_project/pytest/t_test.py::test_asdict
опции
--collect-only только собирать тесты, не выполнять их. ПОКАЗЫВАЕТ список всех тестов

-k ВЫРАЖЕНИЕ       запускать только те тесты, которые соответствуют заданной подстроке
                    Пример:
                        -k 'test_method or test_other' соответствует всем тестам
                        функции и классы, имя которых содержит
                        'test_method' или 'test_other', а -k 'not test_method' соответствует тем, которые не содержат
                        'test_method' в их именах.
-m MARKEXPR        запускает только тесты, соответствующие заданному выражению метки.
                   pytest -m run_these_please -v (такой декоратор есть)
                   Выражение маркера не обязательно должно быть одним маркером. Вы можете использовать такие варианты,
                   как -m "mark1 and mark2" для тестов с обоими маркерами, -m "mark1 and not mark2" для тестов,
                   которые имеют метку 1, но не метку 2, -m "mark1 or mark2" для тестов с одним из и т. д.
-x, --exitfirst    прекращает тестирование при первой ошибке теста - на начальном этапе экономит время на отладке
--maxfail=число    Параметр -x приводит к остановке после первого отказа теста. Если вы хотите, чтобы некоторые число сбоев было допущено,
                    но не целая тонна, используйте параметр --maxfail, чтобы указать, сколько ошибок допускается получить.

-s и --capture=метод    Флаг -s позволяет печатать операторы — или любой другой вывод, который обычно печатается в stdout,
                        чтобы фактически быть напечатаным в стандартном выводе во время выполнения тестов. Это сокращенный вариант для --capture=no.
                        Смысл в том, что обычно выходные данные захватываются во всех тестах. Неудачные тесты будут выводиться после того, как тест
                        будет протекать в предположении, что выход поможет вам понять, что что то пошло не так. Параметр -s или --capture=no отключает
                        захват выходных данных. При разработке тестов я обычно добавляю несколько операторов print(), чтобы можно было следить за ходом теста.

-lf, --last--failed     При сбое одного или нескольких тестов способ выполнения только неудачных тестов полезен для отладки.
                        Выполнит только последние сбойные тесты, остальные не будет
                        –ff, --failed-first  Параметр  будет делать то же самое, что и --last-failed, а затем выполнять остальные тесты, прошедшие в прошлый раз:

v, --verbose увеличить детализацию - выводит списком прохождение тестов и другое
-q, --quiet уменьшить многословие.
--verbosity=VERBOSE установить многословие

-l, --showlocals  При использовании параметра -l/--showlocals локальные переменные и их значения отображаются вместе с tracebacks для неудачных тестов.

--tb=style  изменяет способ вывода пакетов трассировки для сбоев. При сбое теста pytest отображает список сбоев
            и так называемую обратную трассировку, которая показывает точную строку, в которой произошел сбой.

--durations=N   невероятно полезна, когда вы пытаетесь ускорить свой набор тестов. Она не меняет ваши тесты; сообщает самый медленный N номер
                tests/setups/teardowns по окончании тестов. Если вы передадите --durations=0, он сообщит обо всем в порядке от самого медленного к самому быстрому.


отладка и настройка тестовой сессии:
--basetemp=dir базовый временный каталог для этого тестового запуска. (предупреждение: этот каталог удаляется, если он существует)
--version отображать версию pytest lib и информацию об импорте.
-h, --help показать справочное сообщение и информацию о конфигурации

"""