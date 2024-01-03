from iservmail.iservconnection import IservConnection
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.by import By
# import config
# import config_test
# import pytest


def test_creation():
    """Assert that a connection object is successfully created."""
    con = IservConnection()
    assert isinstance(con, IservConnection)

# import unittest


# class TestIservConnection(unittest.TestCase):

#     def test_creation(self):
#         """Assert that a connection object is successfully created."""
#         con = IservConnection()
#         self.assertIsInstance(con, IservConnection)

#     def test_firefoxConnection(self):
#         """Assert that a connection to firefox can be established."""
#         with IservConnection() as con:
#             self.assertIsInstance(con, IservConnection)

#     def test_firefoxConnectionNonHeadless(self):
#         """Assert that a non-headless connection to firefox can
#         be established."""
#         with IservConnection(headless=False) as con:
#             self.assertIsInstance(con, IservConnection)

#     def test_login(self):
#         """Asserts that IServ login is successful."""
#         with IservConnection() as con:
#             try:
#                 con._login()
#                 username = con.driver.find_element(By.CLASS_NAME,
#                                                    'profile-username')
#                 self.assertEquals(username.text,
#                                   config_test.iserv_full_username,
#                                   "Wrong user!")
#             except NoSuchElementException:
#                 self.fail("Login seems to have failed.")

#     def test_goto_mail(self):
#         """Asserts that mail page in IServ is opened successfully."""
#         with IservConnection() as con:
#             try:
#                 con._login()
#                 con._goto_mail()
#                 con.driver.find_element(By.ID, 'mail-compose')
#             except NoSuchElementException:
#                 self.fail("Mail page not opened correctly.")

#     def test_compose_new_mail(self):
#         """Asserts that new mail form is opened successfully."""
#         with IservConnection() as con:
#             try:
#                 con._login()
#                 con._goto_mail()
#                 con._compose_new_mail()
#                 to_field = con.driver.find_element(
#                     By.XPATH, '/html/body/div/div[2]/div[3]/'
#                     'div[1]/div/div/div/div/div/form/div[1]/'
#                     'div[1]/div[2]/div[1]/label')
#                 self.assertEquals(to_field.text, 'Empfänger')
#             except NoSuchElementException:
#                 self.fail("Mail page not opened correctly.")

#     def test_set_receiver(self):
#         with IservConnection() as con:
#             con._login()
#             con._goto_mail()
#             con._compose_new_mail()
#             con._set_receiver([f"{config.iserv_username}@{config.iserv_url}"])
#             try:
#                 con.driver.find_element(
#                     By.XPATH,
#                     "//div[@class='item'][contains(@data-value,"
#                     f"'{config.iserv_username}@{config.iserv_url}')]"
#                 )
#             except NoSuchElementException:
#                 self.fail("Receiver not set correctly.")

#     def test_set_subject(self):
#         with IservConnection() as con:
#             con._login()
#             con._goto_mail()
#             con._compose_new_mail()
#             con._set_subject("Betreff-Text")
#             subject_field = con.driver.find_element(
#                 By.ID, 'iserv_mail_compose_subject'
#             )
#             self.assertEqual(subject_field.get_attribute('value'),
#                              "Betreff-Text")

#     def test_set_body(self):
#         with IservConnection() as con:
#             con._login()
#             con._goto_mail()
#             con._compose_new_mail()
#             con._set_body("Zeile1\n Zeile2")
#             body_field = con.driver.find_element(
#                 By.ID, 'iserv_mail_compose_content'
#             )
#             self.assertEqual(body_field.get_attribute('value'),
#                              "Zeile1\n Zeile2")

#     def test__send_mail(self):
#         with IservConnection() as con:
#             con._login()
#             con._goto_mail()
#             con._compose_new_mail()
#             con._set_receiver([f"{config_test.iserv_address_for_test}"])
#             con._set_subject("Testmail")
#             con._set_body("Kann gelöscht werden.")
#             con._send_mail()
#             self.assertEqual(con.driver.current_url,
#                              f"{config.iserv_url}/iserv/mail")

#     def test_send_mail(self):
#         with IservConnection() as con:
#             self.assertFalse(
#                 con.send_mail(
#                     receiver=[f"{config_test.outside_address_for_test}"],
#                     subject="Testmail",
#                     body="Kann gelöscht werden."
#                 )
#             )
#             self.assertFalse(
#                 con.send_mail(
#                     receiver=["this_is_not_a_mail_address"],
#                     subject="Testmail",
#                     body="Kann gelöscht werden."
#                 )
#             )
#             self.assertFalse(
#                 con.send_mail(
#                     receiver=[f"{config_test.iserv_address_for_test}",
#                               "this_is_not_a_mail_address"],
#                     subject="Testmail",
#                     body="Kann gelöscht werden."
#                 )
#             )
#             self.assertFalse(
#                 con.send_mail(
#                     receiver=[f"{config_test.outside_address_for_test}",
#                               f"{config_test.iserv_address_for_test}"],
#                     subject="Testmail",
#                     body="Kann gelöscht werden."
#                 )
#             )
#             self.assertTrue(
#                 con.send_mail(
#                     receiver=[f"{config_test.iserv_address_for_test}"],
#                     subject="Testmail",
#                     body="Kann gelöscht werden."
#                 )
#             )

#     def test_fail_without_contextmanager(self):
#         con = IservConnection()
#         self.assertFalse(
#             con.send_mail(
#                 receiver=[f"{config_test.iserv_address_for_test}"],
#                 subject="Testmail",
#                 body="Kann gelöscht werden."
#             )
#         )


# if __name__ == '__main__':
#     unittest.main()
