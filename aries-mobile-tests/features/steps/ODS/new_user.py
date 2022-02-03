from behave import given, when, then
from typing import  TypeVar

T = TypeVar('T')
# None == void/null
# reference
# https://docs.python.org/3/library/typing.html
@given('I am on Get started screen')
def step_1(context:T) -> None:
    print('strongly typed > loosely typed')
