# Create your tests here.
import pytest
from selenium import webdriver

ROOT_URL = "http://localhost:8000"


class TestWithWebDrive:
    driver = webdriver.Chrome()

    def test_go_to_menu(self):
        self.driver.get(ROOT_URL + "/menu/")
        expected_title = "¡Bienvenid@!"
        assert self.driver.title == expected_title

    def test_go_to_login(self):
        self.driver.get(ROOT_URL + "/menu/login/")
        element = self.driver.find_element_by_name("email")
        assert element is not None