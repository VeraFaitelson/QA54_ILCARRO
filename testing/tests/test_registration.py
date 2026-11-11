import uuid
from models.user import User
from pages.registration_page import RegistrationPage


# Сценарий 1: Успешная регистрация с корректными данными
# Создание новой учетной записи при заполнении всех обязательных полей валидными значениями.
# • Тест 1: test_valid_registration_success
# • Шаги: Сгенерировать уникальный Email, заполнить поля Имя (First Name), Фамилия (Last Name),
#   Email (Email), Пароль (Password), отметить чекбокс Условия использования (Terms of Use)
#   и нажать кнопку Отправить (Y'alla!).
# • Ожидаемый результат: Появляется модальное окно с заголовком «Registered» и текстом
#   «You are logged in success». После закрытия окна отображается кнопка Выйти (Log out).
def test_valid_registration_success(driver):
    registration_page = RegistrationPage(driver)
    random_suffix = uuid.uuid4().hex[:8]
    user = User(
        "Vera",
        "Ve",
        f"testvera{random_suffix}@gmail.com",
        "Vera!123456789@"
    )
    registration_page.open_registration_page()
    registration_page.fill_registration_form(user)
    registration_page.click_on_terms_of_use()
    registration_page.click_on_registration_button()
    assert registration_page.confirmation1() == "Registered"
    assert registration_page.confirmation2() == "You are logged in success"
    registration_page.close_window()
    assert registration_page.is_sign_out_displayed()


# Сценарий 2: Неудачная регистрация при пустом поле Имя (First Name)
# Проверка клиентской валидации обязательности заполнения имени пользователя.
# • Тест 2: test_invalid_registration_with_empty_name
# • Шаги: Оставить поле Имя (First Name) пустым (""), заполнить валидными данными Фамилию (Last Name),
#   Email (Email), Пароль (Password) и отметить чекбокс Условия использования (Terms of Use).
# • Ожидаемый результат: Под полем Имя (First Name) появляется ошибка «Name is required»,
#   кнопка отправки формы (Y'alla!) остается неактивной (disabled).
def test_invalid_registration_with_empty_name(driver):
    registration_page = RegistrationPage(driver)
    random_suffix = uuid.uuid4().hex[:8]
    user = User(
        "",
        "Ve",
        f"testvera{random_suffix}@gmail.com",
        "Vera!123456789@"
    )
    registration_page.open_registration_page()
    registration_page.fill_registration_form(user)
    registration_page.click_on_terms_of_use()
    assert registration_page.get_field_error_text() == "Name is required"
    assert registration_page.submit_button_disabled()


# Сценарий 3: Неудачная регистрация из-за некорректного формата Email
# Проверка клиентской валидации формата электронной почты при заполнении формы.
# • Тест 3: test_registration_with_invalid_email_and_valid_password
# • Шаги: Заполнить валидными данными Имя (First Name), Фамилию (Last Name) и Пароль (Password).
#   В поле Email (Email) ввести адрес без символа @ («testveraf1gmail.com») и отметить чекбокс (Terms of Use).
# • Ожидаемый результат: Кнопка отправки формы (Y'alla!) заблокирована (disabled),
#   под полем Email (Email) отображается ошибка «Wrong email format».
def test_registration_with_invalid_email_and_valid_password(driver):
    registration_page = RegistrationPage(driver)
    user = User(
        "Vera",
        "Ve",
        "testveraf1gmail.com",
        "Vera!123456789@"
    )
    registration_page.open_registration_page()
    registration_page.fill_registration_form(user)
    registration_page.click_on_terms_of_use()
    assert registration_page.submit_button_disabled()
    assert registration_page.get_field_error_text() == "Wrong email format"
    assert not registration_page.is_sign_out_displayed()


# Сценарий 4: Неудачная регистрация из-за некорректного формата Пароля
# Проверка клиентской валидации требований безопасности к паролю.
# • Тест 4: test_registration_with_valid_email_and_invalid_password
# • Шаги: Заполнить валидными данными Имя (First Name), Фамилию (Last Name) и Email (Email).
#   В поле Пароль (Password) ввести слишком простой пароль («Vera») и отметить чекбокс (Terms of Use).
# • Ожидаемый результат: Кнопка отправки формы (Y'alla!) заблокирована (disabled),
#   под полем Пароль (Password) отображается ошибка валидации пароля.
def test_registration_with_valid_email_and_invalid_password(driver):
    registration_page = RegistrationPage(driver)
    random_suffix = uuid.uuid4().hex[:8]
    user = User(
        "Vera",
        "Ve",
        f"testvera{random_suffix}@gmail.com",
        "Vera"
    )
    registration_page.open_registration_page()
    registration_page.fill_registration_form(user)
    registration_page.click_on_terms_of_use()
    assert registration_page.submit_button_disabled()
    assert "password" in registration_page.get_field_error_text().lower()
    assert not registration_page.is_sign_out_displayed()


# Сценарий 5: Неудачная регистрация с уже существующим Email
# Проверка серверной обработки попытки повторной регистрации на занятый почтовый адрес.
# • Тест 5: test_registration_with_already_exist_email
# • Шаги: Заполнить форму валидными данными, указав в поле Email (Email) уже зарегистрированный адрес
#   («testveraf@gmail.com»), отметить чекбокс (Terms of Use) и нажать кнопку (Y'alla!).
# • Ожидаемый результат: Появляется модальное окно с заголовком «Registration failed» и текстом
#   «"User already exists"». После закрытия окна кнопка Выйти (Log out) не отображается.
def test_registration_with_already_exist_email(driver):
    registration_page = RegistrationPage(driver)
    user = User(
        "Vera",
        "Ve",
        "testveraf@gmail.com",
        "Vera!123456789@"
    )
    registration_page.open_registration_page()
    registration_page.fill_registration_form(user)
    registration_page.click_on_terms_of_use()
    registration_page.click_on_registration_button()
    assert registration_page.confirmation1() == "Registration failed"
    assert "User already exists" in registration_page.confirmation2()
    registration_page.close_window()
    assert not registration_page.is_sign_out_displayed()
