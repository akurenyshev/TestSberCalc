# -*- coding: utf-8 -*-

import allure
import pytest
import time

TEST_URL = 'http://www.sberbank.ru/ru/quotes/converter'


class TestSberPage(object):

    receive_method_dict = {'card': u'На карту Сбербанка',
                           'account': u'На счет в Сбербанке',
                           'cash': u'Выдать наличные'}
    exchange_method_dict = {'ibank': u'Интернет-банк',
                            'office': u'Отделение (ВСП)',
                            'atm': u'Банкомат / УС'}

    @pytest.mark.test_currency
    def test_currency(self, config):
        """
        The main test for checking currency exchange
        :param config: the config given from config.xml
        :return: nothing

        Step 1: Try to open the page
        Step 2: Wait for elements on the page to be loaded
        Step 3: Collecting used elements
        Step 4: Click the Calculate button
        Step 5: Collecting results
        Step 6: Check results
        """
        def find_child_select(elem, text):
            select = elem.find_element_by_xpath(".//div[@class='select']")
            select.click()
            visible = select.find_element_by_xpath(".//div[@class='visible']")
            options = visible.find_elements_by_xpath(".//span")
            opt_elem = [opt for opt in options if opt.text == text][0]
            return opt_elem

        def normalize_float(num_in_str):
            return float(num_in_str.replace(' ', '').replace(',', '.'))

        AMOUNT = config['amount']
        CURRENCY_IN = config['currency_in']
        CURRENCY_OUT = config['currency_out']
        EXCHANGE_METHOD = config.get('exchange_method', 'ibank')
        RECEIVE_METHOD = config.get('receive_method', 'card')
        with allure.step('Try to open the page {}'.format(TEST_URL)):
            self.driver.get(TEST_URL)
        assert u'Калькулятор иностранных валют' in self.driver.title
        # wait for all frames on the page to be loaded
        with allure.step('Wait to the page load {}'.format(TEST_URL)):
            self.manager.wait_page_load()
        xpath = "//input[contains(@placeholder,'{}')]".format(
            u'Сумма'.encode('utf-8'))
        with allure.step('Try to get all used elements'):
            sum_field = self.driver.find_element_by_xpath(xpath)
            curr_in_div = self.driver.find_element_by_xpath(
                "//div[@data-reactid='.0.$1.$0.0.2']")
            curr_out_div = self.driver.find_element_by_xpath(
                "//div[@data-reactid='.0.$1.$0.0.3']")
            # select the currency in
            curr_in = find_child_select(curr_in_div, CURRENCY_IN)
            curr_in.click()
            # select the currency out
            curr_out = find_child_select(curr_out_div, CURRENCY_OUT)
            curr_out.click()
            # type the amount
            self.manager.set_value(sum_field, AMOUNT)
            # get the costs of the currencies
            buy_cost = self.driver.find_element_by_xpath(
                "//span[@data-reactid='.0.$0.0.0.0.1.$0.2.0']").text
            sell_cost = self.driver.find_element_by_xpath(
                "//span[@data-reactid='.0.$0.0.0.0.1.$0.3.0']").text
            calculate_button = self.driver.find_element_by_xpath(
                "//button[@data-reactid='.0.$1.$0.6.0']")
            receive_radio = self.driver.find_element_by_xpath(
                "//p[contains(.,'{}')]".format(
                    self.receive_method_dict[RECEIVE_METHOD].encode('utf-8')))
            receive_radio.click()
            exchange_radio = self.driver.find_element_by_xpath(
                "//p[contains(.,'{}')]".format(
                    self.exchange_method_dict[EXCHANGE_METHOD].encode('utf-8')))
            exchange_radio.click()
        with allure.step('Try to click the Calculate button'):
            calculate_button.click()
        # result part
        with allure.step('Try to collect results'):
            self.manager.wait_page_load("//span[@data-reactid='.0.$1.$1.1.0']")
            time.sleep(1)
            result_in_curr = self.driver.find_element_by_xpath(
                "//span[@data-reactid='.0.$1.$1.1.1']").text
            result_total = self.driver.find_element_by_xpath(
                "//span[@data-reactid='.0.$1.$1.2.0']").text
            result_out_curr = self.driver.find_element_by_xpath(
                "//span[@data-reactid='.0.$1.$1.2.1']").text
            result_amount = self.driver.find_element_by_xpath(
                "//span[@data-reactid='.0.$1.$1.1.0']").text
        with allure.step('Check results'):
            assert normalize_float(result_amount) == float(AMOUNT)
            assert result_in_curr == CURRENCY_IN
            assert result_out_curr == CURRENCY_OUT
            if 'RUR' in CURRENCY_IN and 'USD' in CURRENCY_OUT:
                result = float(
                    '{0:.2f}'.format(float(AMOUNT) / normalize_float(sell_cost)))
            elif 'USD' in CURRENCY_IN and 'RUR' in CURRENCY_OUT:
                result = float(AMOUNT) * normalize_float(buy_cost)
            assert normalize_float(result_total) == result
