# Create your tests here.
import pytest
from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from lunch_menu.models import Choice, EmployeeChoice, Menu


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

    def login_user(self):
        User.objects.create_user("nora", "nora@cornershop.io", "password")
        self.client.login(username="nora", password="password")
        cookie = self.client.cookies["sessionid"]
        self.selenium.get(self.live_server_url + "/login/")
        self.selenium.add_cookie(
            {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
        )

    def test_go_to_menu(self):
        self.login_user()
        menu = Menu.objects.create(name="Menu name")
        self.selenium.get(self.live_server_url + f"/menu/{menu.id}/")
        expected_title = "¡Bienvenid@!"
        assert self.selenium.title == expected_title

    def test_go_to_login(self):
        self.selenium.get(self.live_server_url + "/login/")
        element = self.selenium.find_element_by_name("password")
        assert element is not None

    def test_create_simple_choice(self):
        self.login_user()
        menu_name = "Example menu"
        menu = Menu.objects.create(name=menu_name)
        choice_description = "Example Meal"
        self.selenium.get(self.live_server_url + f"/menu/{menu.id}/add_choices/")
        self.selenium.find_element_by_id("choice-creation").find_element_by_name(
            "description"
        ).send_keys(choice_description)
        self.selenium.find_element_by_id("choice-creation").find_element_by_id(
            "send"
        ).click()
        choice = Choice.objects.first()
        assert choice.description == choice_description

    def test_create_empty_menu(self):
        self.login_user()
        menu_name = "Example Menu"
        menu_date = "08042021"
        self.selenium.get(self.live_server_url + "/menu/add/")
        self.selenium.find_element_by_id("menu-creation").find_element_by_name(
            "name"
        ).send_keys(menu_name)
        self.selenium.find_element_by_id("menu-creation").find_element_by_name(
            "day"
        ).send_keys(menu_date)
        self.selenium.find_element_by_id("create_menu").click()
        menu = Menu.objects.first()
        assert menu.day.strftime("%m%d%Y") == menu_date
        assert menu_name == menu.name

    def test_employee_see_menu_with_choices_and_select(self):
        menu = Menu.objects.create(name="Example Menu")
        choice_1 = Choice.objects.create(description="Example meal N°1", menu=menu)
        choice_2 = Choice.objects.create(description="Example meal N°2", menu=menu)
        self.selenium.get(self.live_server_url + f"/menu/{menu.id}/")
        text = (
            self.selenium.find_element_by_name("choice")
            .find_element_by_xpath("//option[2]")
            .text
        )
        assert choice_1.description == text
        other_option = self.selenium.find_element_by_name(
            "choice"
        ).find_element_by_xpath("//option[3]")
        other_option.click()
        self.selenium.find_element_by_id("send").click()
        assert (
            self.selenium.current_url
            == self.live_server_url + f"/menu/{menu.id}/employee_choice/"
        )

    def test_see_employees_choices(self):
        self.login_user()
        menu = Menu.objects.create(name="Example Menu")
        choice_1 = Choice.objects.create(description="Example meal N°1", menu=menu)
        choice_2 = Choice.objects.create(description="Example meal N°2", menu=menu)
        EmployeeChoice.objects.create(
            first_name="test4", last_name="test2", choice=choice_1
        )
        EmployeeChoice.objects.create(
            first_name="test5", last_name="test2", choice=choice_2
        )
        self.selenium.get(self.live_server_url + f"/menu/{menu.pk}/choices/")
        web_text_choice_1 = self.selenium.find_element_by_xpath(
            f"//td[contains(text(),'{choice_1.description}')]"
        ).text
        web_text_choice_2 = self.selenium.find_element_by_xpath(
            f"//td[contains(text(),'{choice_2.description}')]"
        ).text
        assert choice_1.description == web_text_choice_1
        assert choice_2.description == web_text_choice_2

    def test_edit_menu(self):
        self.login_user()
        new_name = "Example Menu 2"
        new_date = "08/04/2021"
        menu = Menu.objects.create(name="Example Menu 1")
        self.selenium.get(self.live_server_url + f"/menu/{menu.pk}/change/")
        name_element = self.selenium.find_element_by_id(
            "menu-edit"
        ).find_element_by_name("name")
        day_element = self.selenium.find_element_by_id(
            "menu-edit"
        ).find_element_by_name("day")
        assert menu.name == name_element.text
        assert menu.day.strftime("%m/%d/%Y") == day_element.text
        name_element.send_keys(new_name)
        day_element.send_keys(new_date)
        self.selenium.find_element_by_id("edit_menu").click()
        menu = Menu.objects.first()
        assert menu.day.strftime("%m/%d/%Y") == new_date
        assert new_name == menu.name
