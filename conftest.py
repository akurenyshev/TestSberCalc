# -*- coding: utf-8 -*-
import pytest
import xmltodict

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

CONFIG_PATH = './config.xml'


def load_config(file_name):
    with open(file_name, 'r') as f:
        config_xml = f.read()
    config_dict = xmltodict.parse(config_xml)
    return config_dict['config']


def config_list():
    if CONFIG_PATH:
        tcs = load_config(CONFIG_PATH)
        return [tcs[tc]['name'] for tc in tcs], [tcs[tc] for tc in tcs]


@pytest.fixture(scope='function',
                autouse=True,
                params=config_list()[1],
                ids=config_list()[0])
def config(request):
    return request.param


@pytest.fixture(scope='class', autouse=True)
def manager(request):
    """Fixture which link manager instance for each test class."""
    manager = Manager()
    request.cls.manager = manager

    def get_driver(self):
        return self.manager.driver

    request.cls.driver = property(get_driver)
    yield
    manager.driver.close()


class Manager:
    def __init__(self):
        service_log_path = "./chromedriver.log"
        service_args = ['--verbose']
        self.driver = webdriver.Chrome(service_args=service_args,
                                       service_log_path=service_log_path)
        self.DELAY = 10

    @staticmethod
    def set_value(elem, new_value):
        elem.clear()
        elem.send_keys(new_value)

    def wait_page_load(self, xpath=None):
        if not xpath:
            xpath = "//input[contains(@placeholder,'{}')]".format(
                u'Сумма'.encode('utf-8'))
        try:
            WebDriverWait(self.driver, self.DELAY).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            print "Page is ready!"
        except TimeoutException:
            print "Loading took too much time!"
