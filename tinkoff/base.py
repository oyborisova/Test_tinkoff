from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
import time
import pytest


driver = webdriver.Chrome('/tinkoff/chromedriver')
driver.maximize_window()
wait = WebDriverWait(driver, 180)


def data_test(data):
    conf = json.load(open(str(data), encoding='utf8'))
    return conf

