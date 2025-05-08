from iservmail.iservconnection import IservConnection
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import config
import config_test


def test_creation():
    """Assert that a connection object is successfully created."""
    con = IservConnection()
    assert isinstance(con, IservConnection)


def test_firefoxConnection():
    """Assert that a connection to firefox can be established."""
    with IservConnection() as con:
        assert isinstance(con, IservConnection)


def test_firefoxConnectionNonHeadless():
    """Assert that a non-headless connection to firefox can
    be established."""
    with IservConnection(headless=False) as con:
        assert isinstance(con, IservConnection)


def test_login():
    """Asserts that IServ login is successful."""
    with IservConnection() as con:
        con._login()
        username = con.driver.find_element(By.CLASS_NAME, "profile-username")
        assert username.text == config_test.iserv_full_username


def test_goto_mail():
    """Asserts that mail page in IServ is opened successfully."""
    with IservConnection() as con:
        con._login()
        con._goto_mail()
        # assert if this page contains the text 'Posteingang'
        # and 'fabian.buehler@stoerck-gymnasium.de'
        assert "Posteingang" in con.driver.page_source
        assert config_test.iserv_address_for_test in con.driver.page_source


def test_compose_new_mail():
    """Asserts that new mail form is opened successfully."""
    with IservConnection(headless=False) as con:
        con._login()
        con._goto_mail()
        con._compose_new_mail()

        to_field = con.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[2]/div/"
            "iserv-breadcrumbs/ol/iserv-breadcrumb[3]/li/span",
        )
        assert to_field.text == "Verfassen"


def test_set_receiver():
    """Asserts that receiver can be set correctly."""
    with IservConnection() as con:
        con._login()
        con._goto_mail()
        con._compose_new_mail()
        con._set_receiver([f"{config_test.iserv_address_for_test}"])
        try:
            con.driver.find_element(
                By.XPATH,
                "//div[@class='item'][contains(@data-value,"
                f"'{config_test.iserv_address_for_test}')]",
            )
        except NoSuchElementException:
            assert False


def test_set_subject():
    """Asserts that subject can be set correctly."""
    with IservConnection() as con:
        con._login()
        con._goto_mail()
        con._compose_new_mail()
        con._set_subject("Betreff-Text")
        subject_field = con.driver.find_element(By.ID, "iserv_mail_compose_subject")
        assert subject_field.get_attribute("value") == "Betreff-Text"


def test_change_to_not_formatted():
    """Asserts that text can be changed to not formatted."""
    with IservConnection() as con:
        con._login()
        con._goto_mail()
        con._compose_new_mail()
        con._change_to_not_formatted()
        format_button = con.driver.find_element(By.ID, "iserv_mail_btn_format")
        assert "Formatiert" in format_button.text


def test_set_body():
    """Asserts that body can be set correctly."""
    with IservConnection() as con:
        con._login()
        con._goto_mail()
        con._compose_new_mail()
        con._change_to_not_formatted()
        con._set_body("Zeile1\n Zeile2")
        body_field = con.driver.find_element(By.ID, "iserv_mail_compose_content")
        assert body_field.get_attribute("value") == "Zeile1\n Zeile2"


def test__send_mail():
    """Asserts that mail can be sent correctly."""
    with IservConnection() as con:
        con._login()
        con._goto_mail()
        con._compose_new_mail()
        con._set_receiver([f"{config_test.iserv_address_for_test}"])
        con._set_subject("Testmail")
        con._change_to_not_formatted()
        con._set_body("Kann gelöscht werden.")
        con._send_mail()
        assert con.driver.current_url == (
            f"{config.iserv_url}/iserv/mail/index/"
            "fabian.buehler@stoerck-gymnasium.de/INBOX"
        )


def test_send_mail():
    """Asserts that send_mail method work correctly."""
    with IservConnection() as con:
        assert not con.send_mail(
            receiver=[f"{config_test.outside_address_for_test}"],
            subject="Testmail",
            body="Kann gelöscht werden.",
        )
        assert not con.send_mail(
            receiver=["this_is_not_a_mail_address"],
            subject="Testmail",
            body="Kann gelöscht werden.",
        )
        assert not con.send_mail(
            receiver=[
                f"{config_test.iserv_address_for_test}",
                "this_is_not_a_mail_address",
            ],
            subject="Testmail",
            body="Kann gelöscht werden.",
        )
        assert not con.send_mail(
            receiver=[
                f"{config_test.outside_address_for_test}",
                f"{config_test.iserv_address_for_test}",
            ],
            subject="Testmail",
            body="Kann gelöscht werden.",
        )
        assert con.send_mail(
            receiver=[f"{config_test.iserv_address_for_test}"],
            subject="Testmail",
            body="Kann gelöscht werden.",
        )


def test_fail_without_contextmanager():
    """Asserts that send_mail method fails without context manager."""
    con = IservConnection()
    assert not con.send_mail(
        receiver=[f"{config_test.iserv_address_for_test}"],
        subject="Testmail",
        body="Kann gelöscht werden.",
    )
