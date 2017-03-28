# TestSberCalc
This repo includes selenium tests for
sberbank exchange calc

How to install and run tests:

Install chrome webdriver like said here:
http://blog.likewise.org/2015/01/setting-up-chromedriver-and-the-selenium-webdriver-python-bindings-on-ubuntu-14-dot-04/

Install venv and packages:
1) install python-virtualenv
2) activate venv
3) install with pip: pytest, selenium, xmltodict, pytest-allure-adaptor


Run with command: pytest --alluredir=/var/tmp/allure/ -v -m test_currency
under project dir


