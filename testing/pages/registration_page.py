from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class RegistrationPage:
    LOGIN_LINK = (By.XPATH, "//a[text()='Log in']")
    REGISTRATION_LINK = (By.XPATH, "//a[text()='Click here']")
    NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")
    EMAIL_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    BUTTON_REGISTRATION = (By.CSS_SELECTOR, "button.btn.btn--primary")
    TERMS_OF_USE = (By.NAME, "termsOfUse")
    SIGN_OUT_BUTTON = (By.CSS_SELECTOR, "button.navigation-link.linklike")
    MODAL_BOX = (By.CSS_SELECTOR, "div.modal-content")
    MODAL_TITLE = (By.CSS_SELECTOR, "div.modal-content h3")
    MODAL_TEXT = (By.CSS_SELECTOR, "div.modal-content p")
    MODAL_OK_BUTTON = (By.CSS_SELECTOR, "div.modal-content button.btn--primary")
    FIELD_ERROR = (By.CSS_SELECTOR, "div.error")

    def __init__(self, driver):
        self.driver = driver

    def open_registration_page(self):
        self.driver.find_element(*self.LOGIN_LINK).click()
        self.driver.find_element(*self.REGISTRATION_LINK).click()

    def fill_name_field(self,name):
        self.driver.find_element(*self.NAME).clear()
        self.driver.find_element(*self.NAME).send_keys(name)

    def full_last_name_field(self, last_name):
        self.driver.find_element(*self.LAST_NAME).clear()
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)

    def fill_email_field(self,email):
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def fill_password_field(self,password):
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_on_terms_of_use(self):
        self.driver.find_element(*self.TERMS_OF_USE).click()

    def click_on_registration_button(self):
        self.driver.find_element(*self.BUTTON_REGISTRATION).click()

    def get_modal_title_text(self):
        """Ждет появление модалки и возвращает её заголовок (h3)"""
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.MODAL_TITLE)
        )
        return element.text

    def get_modal_body_text(self):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.MODAL_TEXT)
        )
        return element.text

    def click_ok_button_in_modal(self):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.MODAL_OK_BUTTON)
        )
        element.click()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element_located(self.MODAL_BOX)
        )

    def is_sign_out_displayed(self):
        try:
            WebDriverWait(self.driver, timeout=15).until(
                expected_conditions.visibility_of_element_located(self.SIGN_OUT_BUTTON)
            )
            return True
        except TimeoutException:
            return False

    def get_field_error_text(self):
        element = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.FIELD_ERROR)
        )
        return element.text

    def is_registration_button_enabled(self):
        button = self.driver.find_element(*self.BUTTON_REGISTRATION)
        return button.is_enabled()