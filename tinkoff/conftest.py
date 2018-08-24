from base import *
import pytest


def pytest_addoption(parser):
    parser.addoption("--conf", action="store", default="config")\


@pytest.fixture()
def data(request):
    data = {}
    data.update(data_test(str(request.config.getoption("--conf"))))
    return data