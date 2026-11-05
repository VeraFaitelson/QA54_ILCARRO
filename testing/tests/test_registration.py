import time
from pages.registration_page import RegistrationPage


VALID_NAME = "Vera"
VALID_LAST_NAME = "Ve"
VALID_EMAIL = "testvera1__@gmail.com"
UNIQUE_EMAIL = f"testveraf{int(time.time())}@gmail.com"
VALID_PASSWORD = "Vera!123456789@"
INVALID_EMAIL = "testveraf1gmail.com"
INVALID_PASSWORD = "Vera"
ALREADY_REGISTERED_EMAIL = "testveraf@gmail.com"

def test_valid_registration_success(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_name_field(VALID_NAME)
    registration_page.full_last_name_field(VALID_LAST_NAME)
    registration_page.fill_email_field(UNIQUE_EMAIL)
    registration_page.fill_password_field(VALID_PASSWORD)
    registration_page.click_on_terms_of_use()
    registration_page.click_on_registration_button()
    modal_title = registration_page.get_modal_title_text()
    assert "failed" not in modal_title.lower()
    registration_page.click_ok_button_in_modal()
    assert registration_page.is_sign_out_displayed()


def test_registration_with_invalid_email_and_valid_password(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_name_field(VALID_NAME)
    registration_page.full_last_name_field(VALID_LAST_NAME)
    registration_page.fill_email_field(INVALID_EMAIL)
    registration_page.fill_password_field(VALID_PASSWORD)
    registration_page.click_on_terms_of_use()
    assert not registration_page.is_registration_button_enabled(), "Кнопка регистрации активна, хотя email некорректен!"
    error_text = registration_page.get_field_error_text()
    assert error_text == "Wrong email format"
    assert not registration_page.is_sign_out_displayed()


def test_registration_with_valid_email_and_invalid_password(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_name_field(VALID_NAME)
    registration_page.full_last_name_field(VALID_LAST_NAME)
    registration_page.fill_email_field(VALID_EMAIL)
    registration_page.fill_password_field(INVALID_PASSWORD)
    registration_page.click_on_terms_of_use()
    assert not registration_page.is_registration_button_enabled()
    error_text = registration_page.get_field_error_text()
    assert "password" in error_text.lower()
    assert not registration_page.is_sign_out_displayed()


def test_registration_with_already_exist_email(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open_registration_page()
    registration_page.fill_name_field(VALID_NAME)
    registration_page.full_last_name_field(VALID_LAST_NAME)
    registration_page.fill_email_field(ALREADY_REGISTERED_EMAIL)
    registration_page.fill_password_field(VALID_PASSWORD)
    registration_page.click_on_terms_of_use()
    registration_page.click_on_registration_button()
    modal_title = registration_page.get_modal_title_text()
    assert modal_title == "Registration failed"
    modal_body = registration_page.get_modal_body_text()
    assert "User already exists" in modal_body
    registration_page.click_ok_button_in_modal()
    assert not registration_page.is_sign_out_displayed()