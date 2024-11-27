from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from email_validator import validate_email, EmailNotValidError
import config


class IservConnection():
    def __init__(self, headless=True) -> None:
        self._options = Options()
        self.driver = None
        if headless:
            self._options.add_argument("--headless")

        self.USERNAME = config.iserv_username
        self.PASSWORD = config.iserv_password
        self.iserv_url = config.iserv_url
        self.iserv_allowed_domain = config.iserv_allowed_domain

    def __enter__(self):
        self.driver = webdriver.Firefox(options=self._options)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()

    def _login(self):
        self.driver.get(self.iserv_url)
        try:
            login_username = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/main/div/'
                'div[2]/form/div[2]/input')
            login_password = self.driver.find_element(
                By.XPATH, '//*[@id="password_login"]')
            login_button = self.driver.find_element(
                By.XPATH, '/html/body/div[1]/main/div/div[2]'
                '/form/div[4]/div[1]/button')

            login_username.clear()
            login_username.send_keys(self.USERNAME)
            login_password.clear()
            login_password.send_keys(self.PASSWORD)
            login_button.click()
        except NoSuchElementException as e:
            raise e

    def _goto_mail(self):
        self.driver.get(f"{self.iserv_url}/iserv/mail")

    def _compose_new_mail(self):
        compose_button = next(elem for elem in self.driver.find_elements(
            By.ID, 'mail-compose') if elem.is_displayed())
        compose_button.click()

    def _set_receiver(self, receiver=['']):
        receiver_field = self.driver.find_element(
            By.ID, 'iserv_mail_compose_to-selectized'
        )
        receiver_field.clear()
        for rec in receiver:
            receiver_field.send_keys(rec)
            receiver_field.send_keys(Keys.TAB)

    def _set_subject(self, subject=''):
        subject_field = self.driver.find_element(
            By.ID, 'iserv_mail_compose_subject'
        )
        subject_field.clear()
        subject_field.send_keys(subject)

    def _set_body(self, body=''):
        body_field = self.driver.find_element(
            By.ID, 'iserv_mail_compose_content'
        )
        body_field.clear()
        body_field.send_keys(body)

    def _send_mail(self):
        send_button = self.driver.find_element(
            By.ID, "iserv_mail_compose_actions_send"
        )
        send_button.click()

    def send_mail(self, receiver=None, subject='', body=''):
        if receiver is None:
            return False
        if self.driver is None:
            return False

        receiver_list = []
        for recv in receiver:
            try:
                mail = validate_email(recv, check_deliverability=False)
                if mail.domain != self.iserv_allowed_domain:
                    return False
            except EmailNotValidError:
                return False
            receiver_list.append(mail.normalized)

        self._login()
        self._goto_mail()
        self._compose_new_mail()
        self._set_receiver(receiver_list)
        self._set_subject(subject)
        self._set_body(body)
        self._send_mail()
        return True
