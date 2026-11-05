from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class LoginPage:
    LOGIN_LINK = (By.XPATH, "//a[text()='Log in']")
    EMAIL_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    BUTTON_LOGIN = (By.CSS_SELECTOR, "button.btn.btn--primary")
    MODAL_BOX = (By.CSS_SELECTOR, "div.modal-content")
    MODAL_TITLE = (By.CSS_SELECTOR, "div.modal-content h3")
    MODAL_TEXT = (By.CSS_SELECTOR, "div.modal-content p")
    MODAL_OK_BUTTON = (By.CSS_SELECTOR, "div.modal-content button.btn--primary")
    FIELD_ERROR = (By.CSS_SELECTOR, "div.error")
    SIGN_OUT_BUTTON = (By.CSS_SELECTOR, "button.navigation-link.linklike")

    def __init__(self, driver):
        self.driver = driver

    def open_login_page(self):
        self.driver.find_element(*self.LOGIN_LINK).click()

    def fill_email_field(self, email):
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def fill_password_field(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_on_login_button(self):
        self.driver.find_element(*self.BUTTON_LOGIN).click()

    def get_modal_title_text(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MODAL_TITLE)
        )
        return element.text

    def get_modal_body_text(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MODAL_TEXT)
        )
        return element.text

    def click_ok_button_in_modal(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.MODAL_OK_BUTTON)
        )
        element.click()

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.MODAL_BOX)
        )

    def is_sign_out_displayed(self):
        try:
            WebDriverWait(self.driver, timeout=15).until(
                EC.visibility_of_element_located(self.SIGN_OUT_BUTTON)
            )
            return True
        except TimeoutException:
            return False

    def get_field_error_text(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.FIELD_ERROR)
        )
        return element.text

    def is_login_button_enabled(self):
        button = self.driver.find_element(*self.BUTTON_LOGIN)
        return button.is_enabled()