import uuid
from models.user import User
from pages.login_page import LoginPage


# Сценарий 1: Успешная авторизация с корректными данными
# Вход в личный кабинет при заполнении формы валидными
# данными зарегистрированного пользователя.
# • Тест 1: test_valid_login_success
# • Шаги: Открыть страницу входа, заполнить поля Email (Email)
# и Пароль (Password) корректными данными
#   существующего пользователя и нажать кнопку Отправить (Y'alla!).
# • Ожидаемый результат: Пользователь успешно авторизован,
# в меню отображается кнопка Выйти (Log out).
def test_valid_login_success(driver):
    login_page = LoginPage(driver)
    user = User(
        "Vera",
        "Ve",
        "testvera1__@gmail.com",
        "Vera!123456789@"
    )
    login_page.open_login_page()
    login_page.fill_login_form(user)
    login_page.click_on_login_button()
    assert login_page.is_sign_out_displayed()


# Сценарий 2: Неудачная авторизация из-за некорректного формата Email
# Проверка клиентской валидации формата электронной почты при заполнении формы входа.
# • Тест 2: test_login_with_invalid_email_and_valid_password
# • Шаги: Ввести в поле Email (Email) адрес с нарушением формата
# без символа @ («testveraf1gmail.com»),
#   а в поле Пароль (Password) указать валидный пароль.
# • Ожидаемый результат: Кнопка отправки формы (Y'alla!) заблокирована (disabled),
#   под полем Email (Email) отображается ошибка «Wrong email format»,
#   кнопка Выйти (Log out) не появляется.
def test_login_with_invalid_email_and_valid_password(driver):
    login_page = LoginPage(driver)
    user = User(
        "Vera",
        "Ve",
        "testveraf1gmail.com",
        "Vera!123456789@"
    )
    login_page.open_login_page()
    login_page.fill_login_form(user)
    assert login_page.submit_button_disabled()
    assert login_page.get_field_error_text() == "Wrong email format"
    assert not login_page.is_sign_out_displayed()


# Сценарий 3: Неудачная авторизация из-за неверного Пароля
# Проверка серверной обработки попытки входа с правильным логином, но неверным паролем.
# • Тест 3: test_login_with_valid_email_and_invalid_password
# • Шаги: Ввести зарегистрированный Email (Email), указать неверный короткий Пароль
# (Password) («Vera»)
#   и нажать кнопку Отправить (Y'alla!).
# • Ожидаемый результат: Появляется модальное окно с заголовком «Login failed»
# и сообщением об ошибке
#   неверного логина или пароля. После закрытия окна кнопка Выйти (Log out)
#   не отображается.
def test_login_with_valid_email_and_invalid_password(driver):
    login_page = LoginPage(driver)
    user = User(
        "Vera",
        "Ve",
        "testvera1__@gmail.com",
        "Vera"
    )
    login_page.open_login_page()
    login_page.fill_login_form(user)
    login_page.click_on_login_button()
    assert login_page.confirmation1() == "Login failed"
    assert "incorrect" in login_page.confirmation2().lower()
    login_page.close_window()
    assert not login_page.is_sign_out_displayed()


# Сценарий 4: Неудачная авторизация с незарегистрированным Email
# Проверка серверной реакции при попытке входа под несуществующей учетной записью.
# • Тест 4: test_login_with_unregistered_email
# • Шаги: Сгенерировать несуществующий в базе Email (Email),
# ввести валидный Пароль (Password)
#   и нажать кнопку Отправить (Y'alla!).
# • Ожидаемый результат: Появляется модальное окно с заголовком «Login failed» и текстом
#   «"Login or Password incorrect"». После закрытия окна кнопка
#   Выйти (Log out) не отображается.
def test_login_with_unregistered_email(driver):
    login_page = LoginPage(driver)
    random_suffix = uuid.uuid4().hex[:8]
    user = User(
        "Vera",
        "Ve",
        f"testveraf{random_suffix}@gmail.com",
        "Vera!123456789@"
    )
    login_page.open_login_page()
    login_page.fill_login_form(user)
    login_page.click_on_login_button()
    assert login_page.confirmation1() == "Login failed"
    assert "Login or Password incorrect" in login_page.confirmation2()
    login_page.close_window()
    assert not login_page.is_sign_out_displayed()