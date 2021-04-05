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

