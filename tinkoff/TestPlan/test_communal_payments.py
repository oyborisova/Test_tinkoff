from Tests.PaymentsTest.communal_payments import *
import pytest


@pytest.allure.testcase('Оплата ЖКУ в Москве')
def test_payment_gku_in_moscow(data):
    payment_gku_in_moscow(data)
