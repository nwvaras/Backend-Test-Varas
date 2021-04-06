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

    def test_create_simple_choice(self):
        self.driver.get(ROOT_URL + "/menu/choices/")
        element = self.driver.find_element_by_id("choice-creation") \
            .find_element_by_name("description").send_keys("Example Meal")
        save_button = self.driver.find_element_by_id("choice-creation").find_element_by_id("send").click()

    def test_create_simple_menu(self):
        self.driver.get(ROOT_URL + "/menu/")
        element = self.driver.find_element_by_id("menu-creation").find_element_by_name("name").send_keys("Example Menu")
        assert element is None
