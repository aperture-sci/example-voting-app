import os
import time

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    InvalidSelectorException,
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotInteractableException,
    WebDriverException)

vote_endpoint = os.getenv('VOTE_ENDPOINT')
result_endpoint = os.getenv('RESULT_ENDPOINT')

# Give Selenium Hub time to start
time.sleep(15)  # TODO: figure how to do this better

@pytest.fixture(scope='module')

def browser():   
    chrome_options = webdriver.ChromeOptions()
    browser = webdriver.Remote(
        command_executor='http://selenium-router:4444/wd/hub',
        options=chrome_options
    )
    
    yield browser
    browser.quit()

def test_confirm_vote_title(browser):
    browser.get("http://{}".format(vote_endpoint))
    option_a = "Cats"
    option_b = "Dogs"
    assert "{} vs {}!".format(option_a, option_b) in browser.title

def test_confirm_vote_choice_form(browser):
    browser.get("http://{}".format(vote_endpoint))
    element = browser.find_element(By.ID, 'choice')
    assert element.get_attribute('id') == 'choice'


def test_confirm_vote_button_a(browser):
    browser.get("http://{}".format(vote_endpoint))
    element = browser.find_element(By.ID, 'a')
    assert element.get_attribute('id') == 'a'


def test_confirm_vote_button_b(browser):
    browser.get("http://{}".format(vote_endpoint))
    element = browser.find_element(By.ID, 'b')
    assert element.get_attribute('id') == 'b'


def test_vote_click(browser,):
    browser.get("http://{}".format(vote_endpoint))
    browser.find_element(By.ID, 'a').click()
    WebDriverWait(browser, 3)


def test_confirm_result_title(browser):
    browser.get("http://{}".format(result_endpoint))
    assert "Cats vs Dogs -- Result" in browser.title


def test_confirm_result(browser):
    browser.get("http://{}".format(result_endpoint))
    element = browser.find_element(By.ID, 'result')
    assert element.get_attribute('id') == 'result'


def test_confirm_result_vote_tally(browser):
    browser.get("http://{}".format(result_endpoint))
    element = browser.find_element(By.ID, 'result')
    assert 'No votes yet' not in element.text
