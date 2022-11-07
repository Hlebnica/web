from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randint


class SeleniumTests(LiveServerTestCase):
    def test_form_registration(self):
        try:
            driver = webdriver.Chrome()
            driver.get('http://127.0.0.1:8000/book/register')

            user_registration = driver.find_element(By.ID, 'id_login')
            password_registration = driver.find_element(By.ID, 'id_password')
            email_registration = driver.find_element(By.ID, 'id_email')
            handle_registration = driver.find_element(By.ID, 'id_handle')
            role_registration = driver.find_element(By.ID, 'id_role')

            submit = driver.find_element(By.ID, 'register_form_button')

            random_number = randint(1, 9999999999999999)
            user_registration.send_keys(f'SeleniumTest{random_number}')
            password_registration.send_keys(f'SeleniumTest{random_number}')
            email_registration.send_keys(f'SeleniumTest{random_number}')
            handle_registration.send_keys(f'SeleniumTest{random_number}')
            role_registration.send_keys('user')

            submit.send_keys(Keys.RETURN)

            assert driver.current_url == 'http://127.0.0.1:8000/book/login'
        finally:
            print('Test 1 end')

    def test_form_login(self):
        try:
            driver = webdriver.Chrome()
            driver.get('http://127.0.0.1:8000/book/login')

            login_login = driver.find_element(By.ID, 'login')
            password_login = driver.find_element(By.ID, 'password')

            submit = driver.find_element(By.ID, 'sign_in_button')

            login_login.send_keys('SeleniumTest1')
            password_login.send_keys('SeleniumTest1')

            submit.send_keys(Keys.RETURN)

            assert driver.current_url == 'http://127.0.0.1:8000/book/'

        finally:
            print('Test 2 end')
