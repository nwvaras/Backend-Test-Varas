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
        menu_name = "Example menu"
        Menu.objects.create(name=menu_name)
        choice_description = "Example Meal"
        self.selenium.get(self.live_server_url + "/menu/choices/")
        self.selenium.find_element_by_id("choice-creation").find_element_by_name("description").send_keys(
            choice_description)
        self.selenium.find_element_by_id("choice-creation").find_element_by_id("send").click()
        choice = Choice.objects.first()
        assert choice.description == choice_description

    def test_create_empty_menu(self):
        menu_name = "Example Menu"
        menu_date = "08042021"
        self.selenium.get(self.live_server_url + "/menu/")
        self.selenium.find_element_by_id("menu-creation").find_element_by_name("name").send_keys(menu_name)
        self.selenium.find_element_by_id("menu-creation").find_element_by_name("day").send_keys(menu_date)
        self.selenium.find_element_by_id("create_menu").click()
        menu = Menu.objects.first()
        assert menu.day.strftime('%m%d%Y') == menu_date
        assert menu_name == menu.name

    def test_employee_see_menu_with_choices_and_select(self):
        menu = Menu.objects.create(name="Example Menu")
        choice_1 = Choice.objects.create(description="Example meal N°1", menu=menu)
        choice_2 = Choice.objects.create(description="Example meal N°2", menu=menu)
        employee = Employee.objects.create(first_name="test", last_name="selenium", slack_id="slack")
        EmployeeMenuChoice.objects.create(employee=employee, choice=choice_1)
        self.selenium.get(self.live_server_url + f"/menu/employee/{employee.id}/menu_list/")
        text = self.selenium.find_element_by_name("choice").find_element_by_xpath("//option[2]").text
        assert choice_1.description == text
        other_option = self.selenium.find_element_by_name("choice").find_element_by_xpath("//option[3]")
        other_option_text = other_option.text
        other_option.click()
        self.selenium.find_element_by_id("send").click()
        assert self.selenium.current_url == self.live_server_url + f"/menu/employee/{employee.id}/select/"
        assert choice_2.description == other_option_text

    def test_see_employees_choices(self):
        menu = Menu.objects.create(name="Example Menu")
        choice_1 = Choice.objects.create(description="Example meal N°1", menu=menu)
        choice_2 = Choice.objects.create(description="Example meal N°2", menu=menu)
        employee = Employee.objects.create(first_name="Vladimir", last_name="Cortes", slack_id="slack1")
        employee_2 = Employee.objects.create(first_name="Nicolas", last_name="Varas", slack_id="slack2")
        EmployeeMenuChoice.objects.create(employee=employee, choice=choice_1)
        EmployeeMenuChoice.objects.create(employee=employee_2, choice=choice_2)
        self.selenium.get(self.live_server_url + f"/menu/view/{menu.pk}/")
        web_text_choice_1 = self.selenium.find_element_by_xpath(f"//td[contains(text(),'{choice_1.description}')]").text
        web_text_choice_2 = self.selenium.find_element_by_xpath(f"//td[contains(text(),'{choice_2.description}')]").text
        assert choice_1.description == web_text_choice_1
        assert choice_2.description == web_text_choice_2
