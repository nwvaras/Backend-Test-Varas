# Create your tests here.
import pytest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT_URL = "http://localhost:8081"


def set_chrome_options():
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.experimental_options["prefs"] = {}
    return chrome_options


class TestWithWebDrive(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome(options=set_chrome_options())
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_go_to_menu(self):
        self.selenium.get(self.live_server_url + "/menu/")
        expected_title = "¡Bienvenid@!"
        assert self.selenium.title == expected_title

    def test_go_to_login(self):
        self.selenium.get(self.live_server_url + "/menu/login/")
        element = self.selenium.find_element_by_name("email")
        assert element is not None

    def test_create_simple_choice(self):
        self.selenium.get(self.live_server_url + "/menu/choices/")
        element = self.selenium.find_element_by_id("choice-creation").find_element_by_name("description").send_keys(
            "Example Meal")
        save_button = self.selenium.find_element_by_id("choice-creation").find_element_by_id("send").click()

    def test_create_simple_menu(self):
        self.selenium.get(self.live_server_url + "/menu/")
        element = self.selenium.find_element_by_id("menu-creation").find_element_by_name("name").send_keys("Example Menu")
        assert element is None
