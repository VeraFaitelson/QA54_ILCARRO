import time
from pages.login_page import LoginPage

VALID_EMAIL = "testvera1__@gmail.com"
VALID_PASSWORD = "Vera!123456789@"
INVALID_EMAIL = "testveraf1gmail.com"
INVALID_PASSWORD = "Vera"
UNREGISTERED_EMAIL = f"testveraf{int(time.time())}@gmail.com"


def test_valid_login_success(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.fill_email_field(VALID_EMAIL)
    login_page.fill_password_field(VALID_PASSWORD)
    login_page.click_on_login_button()
    assert login_page.is_sign_out_displayed()


def test_login_with_invalid_email_and_valid_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.fill_email_field(INVALID_EMAIL)
    login_page.fill_password_field(VALID_PASSWORD)

    assert not login_page.is_login_button_enabled()
    error_text = login_page.get_field_error_text()
    assert error_text == "Wrong email format"
    assert not login_page.is_sign_out_displayed()


def test_login_with_valid_email_and_invalid_password(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.fill_email_field(VALID_EMAIL)
    login_page.fill_password_field(INVALID_PASSWORD)
    login_page.click_on_login_button()

    modal_title = login_page.get_modal_title_text()
    assert modal_title == "Login failed"
    modal_body = login_page.get_modal_body_text()
    assert "incorrect" in modal_body.lower()
    login_page.click_ok_button_in_modal()
    assert not login_page.is_sign_out_displayed()


def test_login_with_already_exist_email(driver):
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.fill_email_field(UNREGISTERED_EMAIL)
    login_page.fill_password_field(VALID_PASSWORD)
    login_page.click_on_login_button()

    modal_title = login_page.get_modal_title_text()
    assert modal_title == "Login failed"
    modal_body = login_page.get_modal_body_text()
    assert "Login or Password incorrect" in modal_body
    login_page.click_ok_button_in_modal()
    assert not login_page.is_sign_out_displayed()