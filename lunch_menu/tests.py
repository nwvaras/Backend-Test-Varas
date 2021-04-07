# Create your tests here.
import pytest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from lunch_menu.models import Choice, Menu, Employee, EmployeeMenuChoice


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
        choice_description = "Example Meal"
        self.selenium.get(self.live_server_url + "/menu/choices/")
        self.selenium.find_element_by_id("choice-creation").find_element_by_name("description").send_keys(
            choice_description)
        self.selenium.find_element_by_id("choice-creation").find_element_by_id("send").click()
        choice = Choice.objects.first()
        assert choice.description == choice_description

    def test_create_simple_menu(self):
        choice = Choice.objects.create(description="Example meal")
        self.selenium.get(self.live_server_url + "/menu/")
        self.selenium.find_element_by_id("menu-creation").find_element_by_name("name").send_keys("Example Menu")
        text = self.selenium.find_element_by_id("menu-creation").find_element_by_name(
            "choices").find_element_by_xpath("//option[1]").text
        assert choice.description == text

    def test_employee_see_menu_with_choices(self):
        choice_1 = Choice.objects.create(description="Example meal N°1")
        choice_2 = Choice.objects.create(description="Example meal N°2")
        menu = Menu.objects.create(name="Example Menu")
        employee = Employee.objects.create(first_name="test", last_name="selenium", slack_id="slack")
        EmployeeMenuChoice.objects.create(employee=employee, menu=menu)
        menu.choices.add(choice_1)
        menu.choices.add(choice_2)
        self.selenium.get(self.live_server_url + f"/menu/employee/{employee.id}/menu_list/")
        text = self.selenium.find_element_by_name("choice").find_element_by_xpath("//option[2]").text
        assert choice_1.description == text
        self.selenium.find_element_by_id("send").click()
        assert self.selenium.current_url == self.live_server_url + f"/menu/employee/{employee.id}/select/"
