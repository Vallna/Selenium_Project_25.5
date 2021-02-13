import pytest
from selenium import webdriver  # подключение библиотеки
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from setting import valid_email, valid_password

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome(r'C:\ChromeDriver\chromedriver.exe')
    pytest.driver.set_window_size(1400, 1000)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    yield
    pytest.driver.quit()



def test_show_my_pets():
    """Проверка карточек питомцев, используется неявное ожидание"""

    pytest.driver.implicitly_wait(10)

    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    # Переходим на страницу мои питомцы.
    pytest.driver.find_element_by_css_selector('#navbarNav ul li:nth-of-type(1)>a[href="/my_pets"]').click()

    # В эту переменную записали все фото.
    images = pytest.driver.find_elements_by_css_selector('table.table-hover img')
    # В эту переменную записали все имена питомомцев.
    names = pytest.driver.find_elements_by_css_selector('div#all_my_pets tr > td:nth-of-type(1)')
    # Здесь вид питомцев.
    breed_pet = pytest.driver.find_elements_by_css_selector('div#all_my_pets tr > td:nth-of-type(2)')
    # Здесь возраст питомомцев.
    age_pet = pytest.driver.find_elements_by_css_selector('div#all_my_pets tr > td:nth-of-type(3)')

    # Убедиться, что списки содержат хотя бы один елемент.
    assert len(images) != 0
    assert len(names) != 0
    assert len(breed_pet) != 0
    assert len(age_pet) != 0

    for i in range(len(images)):
        photo_src = images[i].get_attribute('src')
        assert photo_src != ''  # если есть фото значит есть атрибут "src"

    for i in range(len(names)):
        assert names[i].text != ''  # чтобы проверить наличие имени, text не пустой

    for i in range(len(age_pet)):
        assert age_pet[i].text != ''  # проверяем что там где указан возраст есть текст

    for i in range(len(breed_pet)):
        assert breed_pet[i].text != ''  # проверяем что там где указан вид есть текст

    # Проверяем, что все питомцы имеют разные имена.
    assert len(set(names)) == len(names)


def get_row_count_from_stats():
    """Получает количество питомцев из блока статистики. Вспомогательный метод"""
    wait = WebDriverWait(pytest.driver, 5)
    text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.\\.col-sm-4'))).text

    parts = text.split('\n')
    found = None
    for part in parts:
        if "Питомцев:" in part:
            found = part
            break

    assert found is not None

    row_count_str = found.split(':')[1]
    row_count = int(row_count_str)
    return row_count

def test_table_my_pets():
    """Проверка таблицы питомцев, используется явное ожидание."""
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    # Переходим на страницу мои питомцы.
    pytest.driver.find_element_by_css_selector('#navbarNav ul li:nth-of-type(1)>a[href="/my_pets"]').click()

    wait = WebDriverWait(pytest.driver, 5)
    all_my_pets = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#all_my_pets table tbody tr")))
    images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.table-hover img")))

    # Убедиться, что списки содержат хотя бы один елемент.
    assert len(all_my_pets) != 0
    assert len(images) != 0

    # Проверить, что количество питомцев соответствует информации в статистике.
    row_count = get_row_count_from_stats()
    assert len(all_my_pets) == row_count

    # Проверяем, что больше чем у половины карточек есть фото.
    assert len(images) > len(all_my_pets) // 2


# python -m pytest -v --driver Chrome --driver-path C:\ChromeDriver\chromedriver.exe test_selenium_petfriends1.py

